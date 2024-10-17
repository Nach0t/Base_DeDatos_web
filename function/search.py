from flask import Blueprint, render_template, request
from sqlalchemy.orm import sessionmaker
from database.DataBase import Student, Teacher, Course, GradeRecord, Faculty, Career  # Ajusta según tus modelos
from sqlalchemy import create_engine

search_blueprint = Blueprint('search', __name__)

# Database connection
engine = create_engine('mysql://root:rootpass@localhost:3306/universitydb')  # Reemplaza con tu URI de conexión
Session = sessionmaker(bind=engine)

@search_blueprint.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')

    results = {
        'students': [],
        'teachers': [],
        'courses': [],
        'grades': [],
        'faculty_students': [],
        'faculty_teachers': []
    }

    if query:
        with Session() as session:
            # Search in the students table
            results['students'] = session.query(Student).filter(
                (Student.first_name.like(f'%{query}%')) | (Student.last_name.like(f'%{query}%'))
            ).all()

            # Search in the teachers table
            results['teachers'] = session.query(Teacher).filter(
                (Teacher.first_name.like(f'%{query}%')) | (Teacher.last_name.like(f'%{query}%'))
            ).all()

            # Search in the courses table
            results['courses'] = session.query(Course).filter(
                Course.name.like(f'%{query}%')
            ).all()

            # Search in the grades table
            results['grades'] = session.query(
                Student.first_name, Student.last_name, Course.name, GradeRecord.grade
            ).join(GradeRecord, Student.id == GradeRecord.student_id).join(Course, Course.id == GradeRecord.course_id).filter(
                (Student.first_name.like(f'%{query}%')) | 
                (Student.last_name.like(f'%{query}%')) | 
                (Course.name.like(f'%{query}%'))
            ).all()

            # Search faculties by name and show associated students and teachers
            faculties = session.query(Faculty).filter(
                Faculty.name.like(f'%{query}%')
            ).all()

            for faculty in faculties:
                faculty_students = session.query(Student).join(Career).filter(Career.faculty_id == faculty.id).all()
                results['faculty_students'].extend(faculty_students)

                faculty_teachers = session.query(Teacher).join(Career).filter(Career.faculty_id == faculty.id).all()
                results['faculty_teachers'].extend(faculty_teachers)

    return render_template('application.html', results=results)
