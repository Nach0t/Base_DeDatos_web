from flask import render_template, request
from sqlalchemy.orm import sessionmaker
from database.DataBase import Faculty, Teacher, Student, Course, GradeRecord
from sqlalchemy import create_engine

# Crear motor de base de datos y sesión (asegúrate de que el URI de la base de datos sea correcto)
engine = create_engine('mysql+pymysql://root:rootpass@localhost/universitydb')
Session = sessionmaker(bind=engine)
session = Session()

def application_view():
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
        # Buscar estudiantes por nombre o apellido
        results['students'] = session.query(Student).filter(
            (Student.first_name.like(f'%{query}%')) | (Student.last_name.like(f'%{query}%'))
        ).all()

        # Buscar profesores por nombre o apellido
        results['teachers'] = session.query(Teacher).filter(
            (Teacher.first_name.like(f'%{query}%')) | (Teacher.last_name.like(f'%{query}%'))
        ).all()

        # Buscar cursos por nombre
        results['courses'] = session.query(Course).filter(
            Course.name.like(f'%{query}%')
        ).all()

        # Buscar calificaciones basadas en nombre de estudiante, curso o calificación
        results['grades'] = session.query(
            Student.first_name, Student.last_name, Course.name, GradeRecord.grade
        ).join(GradeRecord, Student.id == GradeRecord.student_id).join(Course, GradeRecord.course_id == Course.id).filter(
            (Student.first_name.like(f'%{query}%')) |
            (Student.last_name.like(f'%{query}%')) |
            (Course.name.like(f'%{query}%'))
        ).all()

        # Buscar facultades por nombre y mostrar estudiantes y profesores asociados
        faculties = session.query(Faculty).filter(
            Faculty.name.like(f'%{query}%')
        ).all()

        for faculty in faculties:
            # Obtener todos los estudiantes en la facultad
            faculty_students = session.query(Student).join(Career).filter(Career.faculty_id == faculty.id).all()
            results['faculty_students'].extend(faculty_students)

            # Obtener todos los profesores en la facultad
            faculty_teachers = session.query(Teacher).join(Career).filter(Career.faculty_id == faculty.id).all()
            results['faculty_teachers'].extend(faculty_teachers)

    return render_template('application.html', results=results, query=query)
