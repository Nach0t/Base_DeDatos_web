from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from database.DataBase import University, Faculty, Career, Teacher, Student, Course, Enrollment, GradeRecord, AttendanceRecord
from sqlalchemy import create_engine

# Suponemos que ya existe una función que proporciona una sesión
Session = sessionmaker(bind=create_engine('mysql://root:rootpass@localhost/universitydb'))  # Ajustar según tu configuración
session = Session()

def perform_analysis(query):
    # Diccionario para almacenar los resultados del análisis
    analysis_results = {
        'total_students': 0,
        'mean': 0,
        'std_dev': 0,
        'course_name': '',
        'student_name': ''
    }

    if query:
        # Intentar buscar por curso
        course = session.query(Course).filter(Course.name.like(f'%{query}%')).first()
        
        if course:
            # Obtener todas las calificaciones del curso
            grades = session.query(GradeRecord.grade).filter(GradeRecord.course_id == course.id).all()
            grades = [g.grade for g in grades]  # Extraer solo los valores de las calificaciones
            
            if grades:
                # Calcular la media y la desviación estándar
                total_students = len(grades)
                mean = sum(grades) / total_students
                std_dev = (sum((x - mean) ** 2 for x in grades) / total_students) ** 0.5
                
                # Almacenar los resultados en el diccionario
                analysis_results.update({
                    'total_students': total_students,
                    'mean': round(mean, 2),
                    'std_dev': round(std_dev, 2),
                    'course_name': course.name
                })
        else:
            # Si no se encuentra un curso, intentar buscar por estudiante
            student = session.query(Student).filter(
                (Student.first_name.like(f'%{query}%')) | (Student.last_name.like(f'%{query}%'))
            ).first()
            
            if student:
                # Obtener todas las calificaciones del estudiante
                grades = session.query(GradeRecord.grade).filter(GradeRecord.student_id == student.id).all()
                grades = [g.grade for g in grades]  # Extraer solo los valores de las calificaciones
                
                if grades:
                    # Calcular la media y la desviación estándar
                    total_students = len(grades)
                    mean = sum(grades) / total_students
                    std_dev = (sum((x - mean) ** 2 for x in grades) / total_students) ** 0.5
                    
                    # Almacenar los resultados en el diccionario
                    analysis_results.update({
                        'total_students': total_students,
                        'mean': round(mean, 2),
                        'std_dev': round(std_dev, 2),
                        'student_name': f'{student.first_name} {student.last_name}'
                    })
    
    return analysis_results
