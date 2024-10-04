from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from database.DataBase import University, Faculty, Career, Teacher, Student, Course, Enrollment, GradeRecord, AttendanceRecord
from sqlalchemy import create_engine
from app import app, session

def perform_analysis(query):
    analysis_results = {
        'total_students': 0,
        'mean': 0,
        'std_dev': 0,
        'course_name': '',
        'student_name': ''
    }

    if query:
        # Buscar por curso
        course = session.query(Course).filter(Course.name.like(f'%{query}%')).first()
        
        if course:
            # Obtener todas las calificaciones del curso
            grades = session.query(GradeRecord.grade).filter(GradeRecord.course_id == course.id).all()
            grades = [g[0] for g in grades]  # Convertir a lista de números
            
            if grades:
                analysis_results['total_students'] = len(grades)
                analysis_results['mean'] = round(sum(grades) / len(grades), 2)
                analysis_results['std_dev'] = round((sum((x - analysis_results['mean']) ** 2 for x in grades) / len(grades)) ** 0.5, 2)
                analysis_results['course_name'] = course.name
        else:
            # Buscar por estudiante
            student = session.query(Student).filter(
                (Student.first_name.like(f'%{query}%')) | (Student.last_name.like(f'%{query}%'))
            ).first()
            
            if student:
                # Obtener todas las calificaciones del estudiante
                grades = session.query(GradeRecord.grade).filter(GradeRecord.student_id == student.id).all()
                grades = [g[0] for g in grades]  # Convertir a lista de números
                
                if grades:
                    analysis_results['total_students'] = len(grades)
                    analysis_results['mean'] = round(sum(grades) / len(grades), 2)
                    analysis_results['std_dev'] = round((sum((x - analysis_results['mean']) ** 2 for x in grades) / len(grades)) ** 0.5, 2)
                    analysis_results['student_name'] = f'{student.first_name} {student.last_name}'

    return analysis_results