import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from database.DataBase import University, Faculty, Career, Teacher, Student, Course, Enrollment, GradeRecord, AttendanceRecord
from sqlalchemy import create_engine

# Suponemos que ya existe una función que proporciona una sesión
Session = sessionmaker(bind=create_engine('mysql://root:rootpass@localhost/universitydb'))  # Ajustar según tu configuración
session = Session()

def plot_gaussian(grades, mean, std_dev):
    # Crear un rango de valores para la curva de Gauss
    x = np.linspace(mean - 4*std_dev, mean + 4*std_dev, 100)
    gaussian = (1/(std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean)/std_dev)**2)

    # Crear el gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(x, gaussian, label="Distribución normal (Gauss)", color='blue')

    # Puntos rojos para las calificaciones
    for grade in grades:
        plt.plot(grade, 0, 'ro')  # Puntos en la curva con y = 0

    # Punto verde para el promedio
    plt.plot(mean, 0, 'go', label=f'Promedio ({mean})')

    plt.title('Distribución de Calificaciones')
    plt.xlabel('Calificación')
    plt.ylabel('Densidad de probabilidad')
    plt.legend()

    # Guardar la gráfica en memoria como una imagen PNG
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()

    return img_base64

def perform_analysis(query):
    # Diccionario para almacenar los resultados del análisis
    analysis_results = {
        'total_students': 0,
        'mean': 0,
        'std_dev': 0,
        'course_name': '',
        'student_name': '',
        'gaussian_plot': ''
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
                
                # Generar la gráfica de Gauss
                gaussian_plot = plot_gaussian(grades, mean, std_dev)
                
                # Almacenar los resultados en el diccionario
                analysis_results.update({
                    'total_students': total_students,
                    'mean': round(mean, 2),
                    'std_dev': round(std_dev, 2),
                    'course_name': course.name,
                    'gaussian_plot': gaussian_plot
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
                    
                    # Generar la gráfica de Gauss
                    gaussian_plot = plot_gaussian(grades, mean, std_dev)
                    
                    # Almacenar los resultados en el diccionario
                    analysis_results.update({
                        'total_students': total_students,
                        'mean': round(mean, 2),
                        'std_dev': round(std_dev, 2),
                        'student_name': f'{student.first_name} {student.last_name}',
                        'gaussian_plot': gaussian_plot
                    })
    
    return analysis_results
