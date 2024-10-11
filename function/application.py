from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from database.DataBase import University, Faculty, Career, Teacher, Student, Course, Enrollment, GradeRecord, AttendanceRecord
from sqlalchemy import create_engine, session

def application():
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
        # Search students by first or last name
        results['students'] = session.query(Student).filter(
            (Student.first_name.like(f'%{query}%')) | (Student.last_name.like(f'%{query}%'))
        ).all()

        # Search teachers by first or last name
        results['teachers'] = session.query(Teacher).filter(
            (Teacher.first_name.like(f'%{query}%')) | (Teacher.last_name.like(f'%{query}%'))
        ).all()

        # Search courses by name
        results['courses'] = session.query(Course).filter(
            Course.name.like(f'%{query}%')
        ).all()

        # Search grades based on student name, course name, or grade
        results['grades'] = session.query(
            Student.first_name, Student.last_name, Course.name, GradeRecord.grade
        ).join(GradeRecord, Student.id == GradeRecord.student_id).join(Course, GradeRecord.course_id == Course.id).filter(
            (Student.first_name.like(f'%{query}%')) |
            (Student.last_name.like(f'%{query}%')) |
            (Course.name.like(f'%{query}%'))
        ).all()

        # Search faculties by name and show associated students and teachers
        faculties = session.query(Faculty).filter(
            Faculty.name.like(f'%{query}%')
        ).all()

        for faculty in faculties:
            # Get all students in the faculty
            faculty_students = session.query(Student).join(Career).filter(Career.faculty_id == faculty.id).all()
            results['faculty_students'].extend(faculty_students)

            # Get all teachers in the faculty
            faculty_teachers = session.query(Teacher).join(Career).filter(Career.faculty_id == faculty.id).all()
            results['faculty_teachers'].extend(faculty_teachers)

    return render_template('application.html', results=results, query=query)
