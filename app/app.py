from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from load_db import University, Faculty, Career, Course, Teacher, Evaluation, Enrollment, GradeRecord, Student, AttendanceRecord

import pandas as pd
from io import BytesIO
from datetime import date

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add a secret key for session management (important for flash messages)

# Configuración de la base de datos
config = {
    'host': 'mysql',
    'port': '3306',
    'database_name': 'universitydb',
    'user': 'root',
    'password': 'rootpass'
}
engine = create_engine(
    f'mysql+pymysql://{config["user"]}:{config["password"]}@{config["host"]}:{config["port"]}/{config["database_name"]}', 
    echo=False
)

Session = sessionmaker(bind=engine)
session = Session()

try :
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/university')
    def view_university():
        university = session.query(University).first()
        if not university:
            return render_template('university.html', university=None, faculties=[])
        return render_template('university.html', university=university, faculties=university.faculties)

    @app.route('/faculty/<int:faculty_id>')
    def view_faculty(faculty_id):
        faculty = session.query(Faculty).get(faculty_id)
        if not faculty:
            return "Faculty not found", 404
        return render_template('faculty.html', faculty=faculty, careers=faculty.careers)

    @app.route('/career/<int:career_id>')
    def view_career(career_id):
        career = session.query(Career).get(career_id)
        if not career:
            return "Career not found", 404
        return render_template('career.html', career=career, courses=career.courses)


    @app.route('/course/<int:course_id>')
    def view_course(course_id):
        course = session.query(Course).get(course_id)
        if not course:
            return "Course not found", 404

        # Obtener la asistencia para la semana actual (supongamos que estamos trabajando con la semana 1)
        week_attendance = {}
        for enrollment in course.enrollments:
            for class_number in range(1, course.classes_per_week + 1):
                attendance = session.query(AttendanceRecord).filter_by(
                    student_id=enrollment.student.id,
                    course_id=course_id,
                    week=1,  # Aquí se ajusta la semana según corresponda
                    class_number=class_number
                ).first()
                week_attendance[(enrollment.student.id, class_number)] = attendance.attendance if attendance else False

        return render_template('view_course.html', course=course, evaluations=course.evaluations, week_attendance=week_attendance)



    @app.route('/add_course/<int:career_id>', methods=['GET', 'POST'])
    def add_course(career_id):
        career = session.query(Career).get(career_id)
        if not career:
            return "Career not found", 404

        if request.method == 'POST':
            name = request.form['name']
            teacher_id = request.form['teacher']
            evaluations = request.form.getlist('eval_name')
            percentages = request.form.getlist('eval_percentage')

            if not name or not teacher_id:
                return "Course name and teacher are required.", 400

            try:
                new_course = Course(name=name, teacher_id=int(teacher_id), career=career)
                session.add(new_course)
                session.commit()

                # Add evaluations to the course
                for eval_name, eval_percentage in zip(evaluations, percentages):
                    if eval_name and eval_percentage:
                        try:
                            eval_percentage = float(eval_percentage)
                            new_evaluation = Evaluation(name=eval_name, percentage=eval_percentage, course=new_course)
                            session.add(new_evaluation)
                        except ValueError:
                            return "Invalid percentage value.", 400

                session.commit()
                return redirect(url_for('view_career', career_id=career.id))
            except Exception as e:
                session.rollback()
                return f"An error occurred: {str(e)}", 500

        teachers = session.query(Teacher).filter_by(faculty_id=career.faculty_id).all()
        return render_template('add_course.html', career=career, teachers=teachers)

    @app.route('/add_teacher_redirect/<int:career_id>', methods=['GET', 'POST'])
    def add_teacher_redirect(career_id):
        career = session.query(Career).get(career_id)
        if not career:
            return "Career not found", 404

        faculty = career.faculty

        if request.method == 'POST':
            name = request.form['name']
            last_name = request.form['last_name']
            if not name or not last_name:
                return "Name and last name are required.", 400
            try:
                new_teacher = Teacher(name=name, last_name=last_name, faculty=faculty)
                session.add(new_teacher)
                session.commit()
                return redirect(url_for('add_course', career_id=career.id))
            except Exception as e:
                session.rollback()
                return f"An error occurred: {str(e)}", 500

        return render_template('add_teacher_redirect.html', faculty=faculty, career=career)

    @app.route('/add_grade/<int:student_id>/<int:evaluation_id>/<int:course_id>', methods=['POST'])
    def add_grade(student_id, evaluation_id, course_id):
        grade_value = request.form.get('grade')
        if not grade_value:
            return "Invalid grade", 400

        try:
            # Obtener la inscripción del estudiante en el curso
            enrollment = session.query(Enrollment).filter_by(student_id=student_id, course_id=course_id).first()
            if not enrollment:
                return "Enrollment not found", 404

            # Obtener la evaluación específica para el curso
            grade_record = session.query(GradeRecord).filter_by(student_id=student_id, evaluation_id=evaluation_id).first()
            
            # Si ya existe una calificación, la actualizamos, si no, creamos una nueva
            if grade_record:
                grade_record.grade = float(grade_value)
            else:
                new_grade = GradeRecord(student_id=student_id, evaluation_id=evaluation_id, grade=float(grade_value))
                session.add(new_grade)

            session.commit()  # Guardar o actualizar la calificación

            # Ahora recalculamos el promedio del estudiante para este curso
            total_percentage = 0
            weighted_sum = 0
            grades_entered = 0

            # Obtener todas las evaluaciones para este curso
            course = session.query(Course).get(course_id)
            if not course:
                return "Course not found", 404

            for evaluation in course.evaluations:
                # Obtener la calificación del estudiante en esta evaluación
                grade_record = session.query(GradeRecord).filter_by(student_id=student_id, evaluation_id=evaluation.id).first()
                if grade_record and grade_record.grade is not None:
                    weighted_sum += grade_record.grade * evaluation.percentage / 100
                    total_percentage += evaluation.percentage
                    grades_entered += 1

            # Si todas las calificaciones están presentes y el total de los porcentajes es 100, actualizar el promedio
            if grades_entered == len(course.evaluations) and total_percentage == 100:
                enrollment.average = weighted_sum  # Actualizar el promedio ponderado
            else:
                enrollment.average = 1.0  # Si faltan calificaciones o el porcentaje no es 100, asignar un promedio de 1.0

            session.commit()  # Confirmar los cambios

            # Redirigir al curso donde se encuentra el estudiante
            return redirect(url_for('view_course', course_id=course_id))
        except Exception as e:
            session.rollback()
            return f"An error occurred: {str(e)}", 500

    @app.route('/download_grades/<int:course_id>')
    def download_grades(course_id):
        course = session.query(Course).get(course_id)
        if not course:
            return "Course not found", 404

        data = []
        for enrollment in course.enrollments:
            student = enrollment.student
            grades = {evaluation.name: next((gr.grade for gr in student.grades if gr.evaluation_id == evaluation.id), '') for evaluation in course.evaluations}
            average = sum([gr.grade * (evaluation.percentage / 100) for evaluation in course.evaluations if (gr := next((g for g in student.grades if g.evaluation_id == evaluation.id), None))]) / 1
            row = {
                'Student Name': f"{student.name} {student.last_name}",
                **grades,
                'Average': round(average, 2) if average else ''
            }
            data.append(row)

        # Crear archivo XLSX usando pandas
        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Grades')

        output.seek(0)
        return send_file(output, download_name=f"grades_{course.name}.xlsx", as_attachment=True)

    @app.route('/students')
    def students_page():
        return render_template('students.html')

    @app.route('/students/register', methods=['GET', 'POST'])
    def register_student():
        if request.method == 'POST':
            name = request.form['name']
            last_name = request.form['last_name']
            rut = request.form['rut']
            career_id = request.form['career_id']

            if not name or not last_name or not rut or not career_id:
                return "All fields are required.", 400

            try:
                new_student = Student(name=name, last_name=last_name, career_id=int(career_id))
                session.add(new_student)
                session.commit()
                return redirect(url_for('students_page'))
            except Exception as e:
                session.rollback()
                return f"An error occurred: {str(e)}", 500

        faculties = session.query(Faculty).all()
        return render_template('register_student.html', faculties=faculties)

    @app.route('/get_careers/<int:faculty_id>')
    def get_careers(faculty_id):
        faculty = session.query(Faculty).get(faculty_id)
        if not faculty:
            return {"careers": []}, 404
        
        careers = [{"id": career.id, "name": career.name} for career in faculty.careers]
        return {"careers": careers}

    @app.route('/students/enroll', methods=['GET', 'POST'])
    def enroll_student():
        if request.method == 'POST':
            student_id = request.form['student_id']
            course_ids = request.form.getlist('course_id')  # Obtener una lista de cursos

            if not student_id or not course_ids:
                return "Student and at least one course are required.", 400

            try:
                # Inscribir al estudiante en cada uno de los cursos seleccionados
                for course_id in course_ids:
                    enrollment = Enrollment(
                        student_id=int(student_id),
                        course_id=int(course_id),
                        enrollment_date=date.today(),
                        approval=False
                    )
                    session.add(enrollment)

                session.commit()
                return redirect(url_for('students_page'))
            except Exception as e:
                session.rollback()
                return f"An error occurred: {str(e)}", 500

        students = session.query(Student).all()
        # Obtener cursos por estudiante
        student_courses = {}  # Diccionario de cursos filtrados por carrera
        for student in students:
            # Pasar solo los valores que pueden ser serializados en JSON (id y name)
            student_courses[student.id] = [
                {"id": course.id, "name": course.name} for course in student.career.courses
            ]

        return render_template('enroll_student.html', students=students, student_courses=student_courses)

    @app.route('/mark_attendance/<int:course_id>/<int:week>', methods=['POST'])
    def mark_attendance(course_id, week):
        course = session.query(Course).get(course_id)
        if not course:
            return "Course not found", 404

        # Obtener la lista de estudiantes inscritos en el curso
        students = course.enrollments

        # Recoger los datos de la asistencia (de los radio buttons)
        attendance_data = request.form

        # Guardar la asistencia para cada estudiante
        for enrollment in students:
            for class_number in range(1, course.classes_per_week + 1):
                attendance_key = f"attendance_{enrollment.student.id}_class_{class_number}"
                attendance_value = attendance_data.get(attendance_key)

                if attendance_value:
                    attendance = AttendanceRecord(
                        student_id=enrollment.student.id,
                        course_id=course_id,
                        attendance=attendance_value,  # P o A
                        week=week
                    )
                    session.add(attendance)
        
        # Commit the changes to the database
        session.commit()

        return redirect(url_for('view_course', course_id=course.id))  # Redirige a la página del curso
except:
    print("Conexión fallida")

print("hola")

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
