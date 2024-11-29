from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from load_db import University, Faculty, Career, Course, Teacher, Student, Evaluation, GradeRecord, AttendanceRecord

# Configurar la conexión con la base de datos
config = {'host': 'localhost', 'database_name': 'universitydb', 'user': 'root', 'password': 'rootpass'}
engine = create_engine(f'mysql+pymysql://{config["user"]}:{config["password"]}@{config["host"]}/{config["database_name"]}', echo=False)

Session = sessionmaker(bind=engine)
session = Session()

# Crear la universidad
universidad = University(name="Universidad de Ejemplo")

# Crear facultades
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
profesor_juan = Teacher(name="Juan", last_name="Pérez", faculty=facultad_ingenieria)
profesor_ana = Teacher(name="Ana", last_name="García", faculty=facultad_ciencias)
profesor_pedro = Teacher(name="Pedro", last_name="López", faculty=facultad_ingenieria)
profesor_sara = Teacher(name="Sara", last_name="Martínez", faculty=facultad_ciencias)

# Añadir profesores a las facultades
facultad_ingenieria.teachers = [profesor_juan, profesor_pedro]
facultad_ciencias.teachers = [profesor_ana, profesor_sara]

# Crear cursos para las carreras
curso_algoritmos = Course(name="Algoritmos y Estructuras de Datos", teacher=profesor_juan, career=carrera_informatica)
curso_sistemas = Course(name="Sistemas Operativos", teacher=profesor_juan, career=carrera_informatica)
curso_biologia_molecular = Course(name="Biología Molecular", teacher=profesor_ana, career=carrera_biologia)
curso_quimica_organica = Course(name="Química Orgánica", teacher=profesor_sara, career=carrera_quimica)

# Crear evaluaciones
evaluacion_algoritmos_1 = Evaluation(name="Solemne 1", percentage=40, course=curso_algoritmos)
evaluacion_algoritmos_2 = Evaluation(name="Solemne 2", percentage=60, course=curso_algoritmos)
evaluacion_sistemas_1 = Evaluation(name="Laboratorio 1", percentage=30, course=curso_sistemas)
evaluacion_sistemas_2 = Evaluation(name="Examen Final", percentage=70, course=curso_sistemas)
evaluacion_biologia_1 = Evaluation(name="Control 1", percentage=50, course=curso_biologia_molecular)
evaluacion_quimica_1 = Evaluation(name="Informe 1", percentage=100, course=curso_quimica_organica)

# Añadir evaluaciones a los cursos
curso_algoritmos.evaluations = [evaluacion_algoritmos_1, evaluacion_algoritmos_2]
curso_sistemas.evaluations = [evaluacion_sistemas_1, evaluacion_sistemas_2]
curso_biologia_molecular.evaluations = [evaluacion_biologia_1]
curso_quimica_organica.evaluations = [evaluacion_quimica_1]

# Crear estudiantes
estudiante_info_1 = Student(name="Carlos", last_name="Ramírez", career=carrera_informatica)
estudiante_info_2 = Student(name="María", last_name="Fernández", career=carrera_informatica)
estudiante_bio_1 = Student(name="Lucía", last_name="Hernández", career=carrera_biologia)
estudiante_bio_2 = Student(name="Miguel", last_name="Núñez", career=carrera_biologia)

# Añadir estudiantes a las carreras
carrera_informatica.students = [estudiante_info_1, estudiante_info_2]
carrera_biologia.students = [estudiante_bio_1, estudiante_bio_2]

# Crear registros de notas
nota_carlos_alg1 = GradeRecord(student=estudiante_info_1, evaluation=evaluacion_algoritmos_1, grade=6.5)
nota_carlos_alg2 = GradeRecord(student=estudiante_info_1, evaluation=evaluacion_algoritmos_2, grade=7.0)
nota_maria_alg1 = GradeRecord(student=estudiante_info_2, evaluation=evaluacion_algoritmos_1, grade=5.3)
nota_maria_alg2 = GradeRecord(student=estudiante_info_2, evaluation=evaluacion_algoritmos_2, grade=6.2)

# Añadir registros de notas
evaluacion_algoritmos_1.grade_records = [nota_carlos_alg1, nota_maria_alg1]
evaluacion_algoritmos_2.grade_records = [nota_carlos_alg2, nota_maria_alg2]

# Crear registros de asistencia
asistencia_carlos_alg1 = AttendanceRecord(student=estudiante_info_1, course=curso_algoritmos, week=1, attendance=True)
asistencia_carlos_alg2 = AttendanceRecord(student=estudiante_info_1, course=curso_algoritmos, week=2, attendance=False)
asistencia_maria_alg1 = AttendanceRecord(student=estudiante_info_2, course=curso_algoritmos, week=1, attendance=True)
asistencia_maria_alg2 = AttendanceRecord(student=estudiante_info_2, course=curso_algoritmos, week=2, attendance=True)

# Añadir registros de asistencia
curso_algoritmos.attendances = [asistencia_carlos_alg1, asistencia_carlos_alg2, asistencia_maria_alg1, asistencia_maria_alg2]

# Añadir todos los datos a la sesión y confirmar la transacción
session.add(universidad)
session.commit()

# Cerrar la sesión
session.close()

print("Datos insertados correctamente con evaluaciones.")
