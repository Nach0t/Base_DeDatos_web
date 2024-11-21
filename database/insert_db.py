from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import date
from load_db import University, Faculty, Career, Course, Teacher, Student, Enrollment, Evaluation, GradeRecord, AttendanceRecord
import random
# Configurar la conexión con la base de datos (ajusta esto a tu base de datos)
config = {'host': 'localhost', 'database_name': 'universitydb', 'user': 'root', 'password': 'rootpass'}
engine = create_engine(f'mysql+pymysql://{config["user"]}:{config["password"]}@{config["host"]}/{config["database_name"]}', echo=False)

Session = sessionmaker(bind=engine)
session = Session()

# Crear la universidad
universidad = University(name="Universidad de Ejemplo")

# Crear las facultades
facultad_ingenieria = Faculty(name="Facultad de Ingeniería", university=universidad)
facultad_ciencias = Faculty(name="Facultad de Ciencias", university=universidad)

# Añadir facultades a la universidad
universidad.faculties = [facultad_ingenieria, facultad_ciencias]

# Crear carreras en la Facultad de Ingeniería
carrera_informatica = Career(name="Ingeniería en Informática", faculty=facultad_ingenieria)
carrera_mecanica = Career(name="Ingeniería Mecánica", faculty=facultad_ingenieria)

# Crear carreras en la Facultad de Ciencias
carrera_biologia = Career(name="Biología", faculty=facultad_ciencias)
carrera_quimica = Career(name="Química", faculty=facultad_ciencias)

# Añadir carreras a las facultades
facultad_ingenieria.careers = [carrera_informatica, carrera_mecanica]
facultad_ciencias.careers = [carrera_biologia, carrera_quimica]

# Crear profesores
profesor_juan = Teacher(first_name="Juan", last_name="Pérez", faculty=facultad_ingenieria)
profesor_ana = Teacher(first_name="Ana", last_name="García", faculty=facultad_ciencias)

# Añadir profesores a las facultades
facultad_ingenieria.teachers = [profesor_juan]
facultad_ciencias.teachers = [profesor_ana]

# Crear cursos para la carrera de Ingeniería en Informática
curso_algoritmos = Course(name="Algoritmos y Estructuras de Datos", teacher=profesor_juan, career=carrera_informatica)
curso_sistemas = Course(name="Sistemas Operativos", teacher=profesor_juan, career=carrera_informatica)

# Crear cursos para la carrera de Ingeniería Mecánica
curso_mecanica_basica = Course(name="Mecánica Básica", teacher=profesor_juan, career=carrera_mecanica)
curso_dinamica = Course(name="Dinámica", teacher=profesor_juan, career=carrera_mecanica)

# Crear cursos para la carrera de Biología
curso_genetica = Course(name="Genética", teacher=profesor_ana, career=carrera_biologia)
curso_ecologia = Course(name="Ecología", teacher=profesor_ana, career=carrera_biologia)

# Crear cursos para la carrera de Química
curso_quimica_organica = Course(name="Química Orgánica", teacher=profesor_ana, career=carrera_quimica)
curso_analisis_quimico = Course(name="Análisis Químico", teacher=profesor_ana, career=carrera_quimica)

# Añadir cursos a las carreras
carrera_informatica.courses = [curso_algoritmos, curso_sistemas]
carrera_mecanica.courses = [curso_mecanica_basica, curso_dinamica]
carrera_biologia.courses = [curso_genetica, curso_ecologia]
carrera_quimica.courses = [curso_quimica_organica, curso_analisis_quimico]

# Crear estudiantes para la carrera de Ingeniería en Informática
estudiante_info_1 = Student(first_name="Carlos", father_lastname="Ramírez", mother_lastname="López", career=carrera_informatica)
estudiante_info_2 = Student(first_name="María", father_lastname="Fernández", mother_lastname="Soto", career=carrera_informatica)
estudiante_info_3 = Student(first_name="Luis", father_lastname="Hernández", mother_lastname="Vega", career=carrera_informatica)
estudiante_info_4 = Student(first_name="Ana", father_lastname="Gómez", mother_lastname="Castillo", career=carrera_informatica)

# Crear estudiantes para la carrera de Ingeniería Mecánica
estudiante_meca_1 = Student(first_name="Jorge", father_lastname="Martínez", mother_lastname="Paredes", career=carrera_mecanica)
estudiante_meca_2 = Student(first_name="Sofía", father_lastname="López", mother_lastname="García", career=carrera_mecanica)
estudiante_meca_3 = Student(first_name="Andrés", father_lastname="Vargas", mother_lastname="Romero", career=carrera_mecanica)
estudiante_meca_4 = Student(first_name="Paula", father_lastname="Díaz", mother_lastname="Mora", career=carrera_mecanica)

# Crear estudiantes para la carrera de Biología
estudiante_bio_1 = Student(first_name="Elena", father_lastname="Mendoza", mother_lastname="Ríos", career=carrera_biologia)
estudiante_bio_2 = Student(first_name="Tomás", father_lastname="Castro", mother_lastname="Fuentes", career=carrera_biologia)
estudiante_bio_3 = Student(first_name="Raúl", father_lastname="Navarro", mother_lastname="Salinas", career=carrera_biologia)
estudiante_bio_4 = Student(first_name="Claudia", father_lastname="Pérez", mother_lastname="Reyes", career=carrera_biologia)

# Crear estudiantes para la carrera de Química
estudiante_quim_1 = Student(first_name="Gabriel", father_lastname="Ortiz", mother_lastname="Campos", career=carrera_quimica)
estudiante_quim_2 = Student(first_name="Mónica", father_lastname="Cruz", mother_lastname="Aguilar", career=carrera_quimica)
estudiante_quim_3 = Student(first_name="Daniel", father_lastname="Morales", mother_lastname="Benítez", career=carrera_quimica)
estudiante_quim_4 = Student(first_name="Valeria", father_lastname="Silva", mother_lastname="Pineda", career=carrera_quimica)

# Añadir estudiantes a las carreras
carrera_informatica.students = [estudiante_info_1, estudiante_info_2, estudiante_info_3, estudiante_info_4]
carrera_mecanica.students = [estudiante_meca_1, estudiante_meca_2, estudiante_meca_3, estudiante_meca_4]
carrera_biologia.students = [estudiante_bio_1, estudiante_bio_2, estudiante_bio_3, estudiante_bio_4]
carrera_quimica.students = [estudiante_quim_1, estudiante_quim_2, estudiante_quim_3, estudiante_quim_4]

# Añadir todos los estudiantes a la sesión y confirmar la transacción
session.add_all([
    estudiante_info_1, estudiante_info_2, estudiante_info_3, estudiante_info_4,
    estudiante_meca_1, estudiante_meca_2, estudiante_meca_3, estudiante_meca_4,
    estudiante_bio_1, estudiante_bio_2, estudiante_bio_3, estudiante_bio_4,
    estudiante_quim_1, estudiante_quim_2, estudiante_quim_3, estudiante_quim_4
])

session.commit()

# Función para inscribir un estudiante en cursos de su carrera de forma aleatoria
def inscribir_estudiante_a_cursos(estudiante, num_cursos=2):
    cursos_disponibles = estudiante.career.courses
    cursos_a_inscribir = random.sample(cursos_disponibles, min(num_cursos, len(cursos_disponibles)))
    
    for curso in cursos_a_inscribir:
        enrollment = Enrollment(enrollment_date="2024-11-08", approval=False, student=estudiante, course=curso)
        session.add(enrollment)

# Inscribir cada estudiante a al menos dos cursos de su carrera
for carrera in [carrera_informatica, carrera_mecanica, carrera_biologia, carrera_quimica]:
    for estudiante in carrera.students:
        inscribir_estudiante_a_cursos(estudiante)

# Confirmar la transacción
session.commit()

# Función para generar porcentajes que sumen 100% y terminen en 0 o 5
def generar_porcentajes(num_evaluaciones):
    while True:
        # Generar porcentajes que terminan en 0 o 5
        porcentajes = [random.choice(range(5, 50, 5)) for _ in range(num_evaluaciones - 1)]
        suma_actual = sum(porcentajes)

        # Verificar si la suma actual permite que el último porcentaje termine en 0 o 5 y sume 100%
        porcentaje_final = 100 - suma_actual
        if porcentaje_final >= 5 and porcentaje_final <= 50 and porcentaje_final % 5 == 0:
            porcentajes.append(porcentaje_final)
            return porcentajes

# Función para crear evaluaciones de un curso con la suma de porcentajes igual a 100%
def crear_evaluaciones_para_curso(curso, num_evaluaciones):
    porcentajes = generar_porcentajes(num_evaluaciones)

    # Crear evaluaciones y añadirlas a la sesión
    for i, porcentaje in enumerate(porcentajes, start=1):
        evaluacion = Evaluation(
            course=curso,
            name=f"Solemne {i}",
            percentage=porcentaje
        )
        session.add(evaluacion)

# Crear evaluaciones para cada curso
for carrera in [carrera_informatica, carrera_mecanica, carrera_biologia, carrera_quimica]:
    for curso in carrera.courses:
        num_evaluaciones = random.choice([3, 4])  # Escoger entre 3 o 4 evaluaciones aleatoriamente
        crear_evaluaciones_para_curso(curso, num_evaluaciones)

# Confirmar la transacción
session.commit()

# Función para crear registros de notas para cada evaluación de cada curso en el que esté inscrito un estudiante
def crear_registros_de_notas(estudiante):
    for enrollment in estudiante.enrollments:
        curso = enrollment.course
        for evaluacion in curso.evaluations:
            nota = random.uniform(1, 7)  # Generar una nota aleatoria entre 1.0 y 7.0
            registro_nota = GradeRecord(
                student=estudiante,
                evaluation=evaluacion,
                grade=round(nota, 1)  # Redondear a un decimal
            )
            session.add(registro_nota)

# Crear registros de notas para cada estudiante de cada carrera
for carrera in [carrera_informatica, carrera_mecanica, carrera_biologia, carrera_quimica]:
    for estudiante in carrera.students:
        crear_registros_de_notas(estudiante)

# Confirmar la transacción
session.commit()

# Función para crear registros de asistencia para cada estudiante en cada curso durante cuatro semanas
def crear_registros_de_asistencia(estudiante):
    for enrollment in estudiante.enrollments:
        curso = enrollment.course
        for semana in range(1, 5):  # Crear registros para 4 semanas
            asistencia = random.choice([True, False])  # Generar asistencia aleatoria (True o False)
            registro_asistencia = AttendanceRecord(
                student=estudiante,
                course=curso,
                week=semana,
                attendance=asistencia
            )
            session.add(registro_asistencia)

# Crear registros de asistencia para cada estudiante de cada carrera
for carrera in [carrera_informatica, carrera_mecanica, carrera_biologia, carrera_quimica]:
    for estudiante in carrera.students:
        crear_registros_de_asistencia(estudiante)

# Confirmar la transacción
session.commit()

# Función para calcular la nota final y actualizar la columna de aprobación
def calcular_estado_estudiante(estudiante):
    for enrollment in estudiante.enrollments:
        curso = enrollment.course
        suma_notas = 0
        suma_porcentajes = 0

        # Calcular la nota final del curso basándonos en las evaluaciones
        for evaluacion in curso.evaluations:
            # Obtener el registro de la nota de la evaluación
            registro_nota = session.query(GradeRecord).filter_by(student_id=estudiante.id, evaluation_id=evaluacion.id).first()
            if registro_nota:
                nota = registro_nota.grade
                porcentaje = evaluacion.percentage

                # Sumar la nota multiplicada por su porcentaje
                suma_notas += nota * (porcentaje / 100)
                suma_porcentajes += porcentaje

        # Verificar que la suma de los porcentajes sea 100
        if suma_porcentajes == 100:
            # Determinar si el estudiante aprueba o reprueba
            estado = suma_notas >= 4  # Aprobado si la suma es mayor o igual a 4
            enrollment.approval = estado  # Actualizar la columna 'approval'
        else:
            print(f"Advertencia: Los porcentajes no suman 100% para el curso {curso.name} del estudiante {estudiante.first_name} {estudiante.last_name}")

# Calcular el estado de cada estudiante de cada carrera y actualizar la columna 'approval'
for carrera in [carrera_informatica, carrera_mecanica, carrera_biologia, carrera_quimica]:
    for estudiante in carrera.students:
        calcular_estado_estudiante(estudiante)

# Confirmar la transacción
session.commit()

# Guardar los cambios en la base de datos
session.add(universidad)
session.commit()

# Cerrar sesión
session.close()

print("Datos insertados correctamente.")