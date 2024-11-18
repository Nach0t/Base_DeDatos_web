from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from sqlalchemy.orm import joinedload
from datetime import date
from models import engine, Session, Course, Percentage, Student, Enrollment, AttendanceRecord, GradeRecord, Professor
import pandas as pd
import io

# Flask Application
app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/courses')
def courses():
    session = Session()
    courses = session.query(Course).all()
    session.close()
    return render_template('courses.html', courses=courses)

@app.route('/university')
def university():
    return render_template('university.html')

@app.route('/application', methods=['GET'])
def application():
    query = request.args.get('query', '').strip()
    session = Session()
    results = {
        'students': [],
        'professors': [],
        'courses': [],
        'grades': []
    }

    if query:
        # Search students by name or ID
        results['students'] = session.query(Student).filter(
            (Student.first_name.ilike(f"%{query}%")) |
            (Student.last_name_paternal.ilike(f"%{query}%")) |
            (Student.last_name_maternal.ilike(f"%{query}%")) |
            (Student.rut.ilike(f"%{query}%"))
        ).all()

        # Search professors by name
        results['professors'] = session.query(Professor).filter(
            Professor.name.ilike(f"%{query}%")
        ).all()

        # Search courses by name
        results['courses'] = session.query(Course).filter(
            Course.name.ilike(f"%{query}%")
        ).all()

        # Search grades by student name or ID
        results['grades'] = session.query(GradeRecord).join(Student).join(Percentage).filter(
            (Student.first_name.ilike(f"%{query}%")) |
            (Student.last_name_paternal.ilike(f"%{query}%")) |
            (Student.last_name_maternal.ilike(f"%{query}%")) |
            (Student.rut.ilike(f"%{query}%"))
        ).all()

    session.close()
    return render_template('application.html', query=query, results=results)

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course_name = request.form.get('course_name')
        professor_names = request.form.getlist('professor_name')
        eval_names = request.form.getlist('eval_name')
        eval_percentages = request.form.getlist('eval_percentage')
        eval_percentages = [float(p) for p in eval_percentages]

        if sum(eval_percentages) != 100:
            flash('The total percentage must be exactly 100%. Please adjust the values.')
            return redirect(url_for('add_course'))

        if course_name and eval_names and eval_percentages:
            session = Session()
            new_course = Course(name=course_name)
            session.add(new_course)
            session.commit()

            for professor_name in professor_names:
                existing_professor = session.query(Professor).filter_by(name=professor_name).first()
                if not existing_professor:
                    new_professor = Professor(name=professor_name)
                    session.add(new_professor)
                    session.commit()
                    new_course.professors.append(new_professor)
                else:
                    new_course.professors.append(existing_professor)

            for name, percentage in zip(eval_names, eval_percentages):
                new_percentage = Percentage(name=name, percentage=percentage, course_id=new_course.id)
                session.add(new_percentage)

            session.commit()
            session.close()
            flash('Course, professors, and evaluations added successfully')
            return redirect(url_for('index'))

    return render_template('add_course.html')

@app.route('/course/<int:course_id>')
def course_detail(course_id):
    session = Session()
    course = session.query(Course)\
        .options(joinedload(Course.enrollments)
                 .joinedload(Enrollment.student)
                 .joinedload(Student.grades)
                 .joinedload(GradeRecord.percentage))\
        .options(joinedload(Course.percentages))\
        .options(joinedload(Course.professors))\
        .filter_by(id=course_id).first()

    if not course:
        flash("Course not found.")
        return redirect(url_for('index'))

    percentages = course.percentages
    enrollments = course.enrollments
    professors = course.professors

    # Calculate averages for each student
    for enrollment in enrollments:
        total = 0
        total_percentage = 0
        has_grades = False

        for percentage in percentages:
            grade_record = next((grade for grade in enrollment.student.grades if grade.percentage_id == percentage.id), None)
            if grade_record and grade_record.grade is not None:
                has_grades = True
                total += grade_record.grade * (percentage.percentage / 100)
                total_percentage += percentage.percentage

        # Assign the average to the student if there are valid evaluations
        enrollment.average = round(total, 2) if has_grades else 1.0

    # Close the session after extracting all data
    session.close()

    return render_template(
        'course_detail.html',
        course=course,
        percentages=percentages,
        enrollments=enrollments,
        professors=professors
    )

@app.route('/edit_evaluations/<int:course_id>', methods=['GET'])
def edit_evaluations(course_id):
    session = Session()
    course = session.query(Course).filter_by(id=course_id).first()
    percentages = session.query(Percentage).filter_by(course_id=course_id).all()
    session.close()
    return render_template('edit_evaluations.html', course=course, percentages=percentages)

@app.route('/update_evaluations/<int:course_id>', methods=['POST'])
def update_evaluations(course_id):
    session = Session()
    eval_names = request.form.getlist('eval_name')
    eval_percentages = request.form.getlist('eval_percentage')
    eval_percentages = [float(p) for p in eval_percentages]

    if sum(eval_percentages) != 100:
        flash('The total percentage must be exactly 100%. Please adjust the values.')
        return redirect(url_for('edit_evaluations', course_id=course_id))

    # Delete grades related to the course evaluations
    existing_percentages = session.query(Percentage).filter_by(course_id=course_id).all()
    for percentage in existing_percentages:
        session.query(GradeRecord).filter_by(percentage_id=percentage.id).delete()

    # Delete existing evaluations and add new ones
    session.query(Percentage).filter_by(course_id=course_id).delete()
    for name, percentage in zip(eval_names, eval_percentages):
        new_percentage = Percentage(name=name, percentage=percentage, course_id=course_id)
        session.add(new_percentage)

    session.commit()
    session.close()
    flash('Evaluations updated successfully')
    return redirect(url_for('course_detail', course_id=course_id))

@app.route('/add_student/<int:course_id>', methods=['POST'])
def add_student(course_id):
    rut = request.form.get('rut')
    first_name = request.form.get('first_name')
    last_name_paternal = request.form.get('last_name_paternal')
    last_name_maternal = request.form.get('last_name_maternal')

    if rut and first_name and last_name_paternal and last_name_maternal:
        session = Session()
        existing_student = session.query(Student).filter_by(rut=rut).first()
        if existing_student:
            flash('The student with this ID is already registered.')
        else:
            new_student = Student(
                rut=rut,
                first_name=first_name,
                last_name_paternal=last_name_paternal,
                last_name_maternal=last_name_maternal
            )
            session.add(new_student)
            session.commit()
            new_enrollment = Enrollment(student_id=new_student.id, course_id=course_id, enrollment_date=date.today(), approval=False)
            session.add(new_enrollment)
            session.commit()
            flash('Student added successfully')
        session.close()
    else:
        flash('Please fill in all fields.')
    return redirect(url_for('course_detail', course_id=course_id))

@app.route('/mark_attendance/<int:student_id>/<int:course_id>/<int:week>', methods=['POST'])
def mark_attendance(student_id, course_id, week):
    session = Session()
    attendance = 'attendance' in request.form

    existing_record = session.query(AttendanceRecord).filter_by(student_id=student_id, course_id=course_id, week=week).first()
    if existing_record:
        existing_record.attendance = attendance
    else:
        new_record = AttendanceRecord(student_id=student_id, course_id=course_id, week=week, attendance=attendance)
        session.add(new_record)

    session.commit()
    session.close()
    flash('Attendance recorded successfully')
    return redirect(url_for('course_detail', course_id=course_id))

@app.route('/add_grade/<int:student_id>/<int:percentage_id>/<int:course_id>', methods=['POST'])
def add_grade(student_id, percentage_id, course_id):
    try:
        grade = float(request.form.get('grade'))

        # Handle errors for incorrect input (e.g., 65 -> 6.5)
        if grade > 7.0:
            grade = round(grade / 10, 1)
        elif grade < 1.0:
            grade = 1.0

        session = Session()
        existing_record = session.query(GradeRecord).filter_by(student_id=student_id, percentage_id=percentage_id).first()
        if existing_record:
            existing_record.grade = grade
        else:
            new_grade = GradeRecord(student_id=student_id, percentage_id=percentage_id, grade=grade)
            session.add(new_grade)

        session.commit()
        session.close()
        flash('Grade added successfully')
    except ValueError:
        flash('Please enter a valid grade.')
    return redirect(url_for('course_detail', course_id=course_id))

@app.route('/download_grades/<int:course_id>', methods=['GET'])
def download_grades(course_id):
    session = Session()
    course = session.query(Course).filter_by(id=course_id).first()
    enrollments = course.enrollments
    percentages = course.percentages

    # Create a list to store the data
    data = []
    headers = ['Student'] + [f"{percentage.name} ({percentage.percentage}%)" for percentage in percentages] + ['Average']

    # Fill in the data with student information and their grades
    for enrollment in enrollments:
        student = enrollment.student
        row = [f"{student.first_name} {student.last_name_paternal} {student.last_name_maternal}"]
        total = 0
        has_grades = False
        for percentage in percentages:
            grade_record = next((grade for grade in student.grades if grade.percentage_id == percentage.id), None)
            if grade_record and grade_record.grade is not None:
                row.append(grade_record.grade)
                total += grade_record.grade * (percentage.percentage / 100)
                has_grades = True
            else:
                row.append('')
        row.append(round(total, 2) if has_grades else 1.0)
        data.append(row)

    # Create the DataFrame
    df = pd.DataFrame(data, columns=headers)

    # Save the DataFrame to an Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Grades')
    output.seek(0)

    # Download the file
    session.close()
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name=f'grades_course_{course.name}.xlsx')

if __name__ == '__main__':
    app.run(debug=True)
