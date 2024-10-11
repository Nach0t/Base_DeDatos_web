from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from database.DataBase import University, Faculty, Career, Teacher, Student, Course, Enrollment, GradeRecord, AttendanceRecord
from sqlalchemy import create_engine


import os
import json
from flask import Blueprint, request, render_template

# Crear un blueprint para manejar las rutas de contacto
contact_bp = Blueprint('contact', __name__)

# Directorio para guardar los mails
json_dir = os.path.join('static/jsons/mails')
os.makedirs(json_dir, exist_ok=True)  # Crea el directorio si no existe

@contact_bp.route('/contact')
def contact():
    return render_template('contact.html')

@contact_bp.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Recibir los datos del formulario
        first_name = request.form.get('name')
        last_name = request.form.get('lastname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        reason = request.form.get('reason')
        subject = request.form.get('subject')
        message = request.form.get('message')
        recipient = request.form.get('email-select')

        # Crear el diccionario de datos del formulario
        form_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'reason': reason,
            'subject': subject,
            'message': message,
            'recipient': recipient
        }

        # Ruta del archivo JSON
        json_file_path = os.path.join(json_dir, 'contact_data.json')

        # Leer los datos existentes, si el archivo existe
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as json_file:
                try:
                    data = json.load(json_file)  # Cargar datos existentes
                except json.JSONDecodeError:
                    data = []  # Si hay un error de decodificación, inicializar una lista vacía
        else:
            data = []  # Inicializar una lista vacía si el archivo no existe

        # Agregar el nuevo registro
        data.append(form_data)

        # Guardar los datos en el archivo JSON
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)  # Escribir datos en formato JSON

        return "Form submitted successfully!"
    except Exception as e:
        return f"An error occurred while submitting the form: {e}"
    
