from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DECIMAL, Date, Boolean, Float
from sqlalchemy import text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Configuración de la base de datos
config = {'host': 'localhost', 'database_name': 'universitydb', 'user': 'root', 'password': 'rootpass'}

# Crear el motor de conexión y la base de datos si no existe
engine = create_engine(f'mysql+pymysql://{config["user"]}:{config["password"]}@{config["host"]}', echo=True)

with engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {config['database_name']}"))

# Declarar base para las clases ORM
Base = declarative_base()

# Conectar con la base de datos recién creada
engine = create_engine(f'mysql+pymysql://{config["user"]}:{config["password"]}@{config["host"]}/{config["database_name"]}', echo=True)

# Definición de las tablas

class University(Base):
    __tablename__ = 'university'  # Doble guion bajo en ambos lados
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    faculties = relationship('Faculty', back_populates='university')

class Faculty(Base):
    __tablename__ = 'faculty'  # Doble guion bajo en ambos lados
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    university_id = Column(Integer, ForeignKey('university.id'))
    university = relationship('University', back_populates='faculties')
    careers = relationship('Career', back_populates='faculty')
    teachers = relationship('Teacher', back_populates='faculty')

class Career(Base):
    __tablename__ = 'career'  # Doble guion bajo en ambos lados
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    faculty_id = Column(Integer, ForeignKey('faculty.id'))
    faculty = relationship('Faculty', back_populates='careers')
    students = relationship('Student', back_populates='career')

class Teacher(Base):
    __tablename__ = 'teacher'  # Doble guion bajo en ambos lados
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    faculty_id = Column(Integer, ForeignKey('faculty.id'))
    faculty = relationship('Faculty', back_populates='teachers')
    courses = relationship('Course', back_populates='teacher')

class Student(Base):
    __tablename__ = 'student'  # Doble guion bajo en ambos lados
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    career_id = Column(Integer, ForeignKey('career.id'))
    career = relationship('Career', back_populates='students')
    enrollments = relationship('Enrollment', back_populates='student')
    grades = relationship('GradeRecord', back_populates='student')
    attendances = relationship('AttendanceRecord', back_populates='student')

class Course(Base):
    __tablename__ = 'course'  # Doble guion bajo en ambos lados
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    teacher = relationship('Teacher', back_populates='courses')
    enrollments = relationship('Enrollment', back_populates='course')
    grades = relationship('GradeRecord', back_populates='course')
    attendances = relationship('AttendanceRecord', back_populates='course')

class Enrollment(Base):
    __tablename__ = 'enrollment'  # Doble guion bajo en ambos lados
    id = Column(Integer, primary_key=True, autoincrement=True)
    enrollment_date = Column(Date, nullable=False)
    approval = Column(Boolean, nullable=False)
    student_id = Column(Integer, ForeignKey('student.id'))
    course_id = Column(Integer, ForeignKey('course.id'))
    student = relationship('Student', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')

class GradeRecord(Base):
    __tablename__ = 'grade_record'  # Doble guion bajo en ambos lados
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    course_id = Column(Integer, ForeignKey('course.id'))
    grade = Column(Float)
    student = relationship('Student', back_populates='grades')
    course = relationship('Course', back_populates='grades')

class AttendanceRecord(Base):
    __tablename__ = 'attendance_record'  # Doble guion bajo en ambos lados
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    course_id = Column(Integer, ForeignKey('course.id'))
    attendance = Column(Boolean)
    student = relationship('Student', back_populates='attendances')
    course = relationship('Course', back_populates='attendances')


# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Crear una sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()

# Insertar datos en las tablas


# Datos de universidades
university_data = [
    {'name': 'University of Technology'},
    {'name': 'Global Business University'},
    {'name': 'National Academy of Arts'}
]

for data in university_data:
    university = University(**data)
    session.add(university)
session.commit()

# Datos de facultades
faculty_data = [
    {'name': 'Engineering', 'university_id': 1},
    {'name': 'Computer Science', 'university_id': 1},
    {'name': 'Business Administration', 'university_id': 2},
    {'name': 'Finance', 'university_id': 2},
    {'name': 'Painting', 'university_id': 3},
    {'name': 'Sculpture', 'university_id': 3}
]

for data in faculty_data:
    faculty = Faculty(**data)
    session.add(faculty)
session.commit()

# Datos de carreras
career_data = [
    {'name': 'Software Engineering', 'faculty_id': 2},
    {'name': 'Mechanical Engineering', 'faculty_id': 1},
    {'name': 'International Business', 'faculty_id': 3},
    {'name': 'Corporate Finance', 'faculty_id': 4},
    {'name': 'Fine Arts', 'faculty_id': 5},
    {'name': 'Art Restoration', 'faculty_id': 6}
]

for data in career_data:
    career = Career(**data)
    session.add(career)
session.commit()

# Datos de profesores (algunos compartidos)
teacher_data = [
    {'first_name': 'Carlos', 'last_name': 'Garcia', 'faculty_id': 1},
    {'first_name': 'Laura', 'last_name': 'Diaz', 'faculty_id': 2},
    {'first_name': 'Fernando', 'last_name': 'Gomez', 'faculty_id': 3},
    {'first_name': 'Clara', 'last_name': 'Sanchez', 'faculty_id': 4},
    {'first_name': 'Carlos', 'last_name': 'Garcia', 'faculty_id': 2},
    {'first_name': 'Sofia', 'last_name': 'Martinez', 'faculty_id': 5}
]

for data in teacher_data:
    teacher = Teacher(**data)
    session.add(teacher)
session.commit()

# Datos de cursos
course_data = [
    {'name': 'Data Structures', 'teacher_id': 2},
    {'name': 'Mechanical Design', 'teacher_id': 1},
    {'name': 'Corporate Strategy', 'teacher_id': 3},
    {'name': 'Financial Analysis', 'teacher_id': 4},
    {'name': 'Advanced Painting', 'teacher_id': 6}
]

for data in course_data:
    course = Course(**data)
    session.add(course)
session.commit()

# Datos de estudiantes
student_data = [
    {'first_name': 'Jose', 'last_name': 'Martinez', 'career_id': 1},
    {'first_name': 'Luisa', 'last_name': 'Fernandez', 'career_id': 2},
    {'first_name': 'Diego', 'last_name': 'Gonzalez', 'career_id': 3},
    {'first_name': 'Ana', 'last_name': 'Morales', 'career_id': 4},
    {'first_name': 'Lucia', 'last_name': 'Jimenez', 'career_id': 5},
    {'first_name': 'Raul', 'last_name': 'Torres', 'career_id': 6}
]

for data in student_data:
    student = Student(**data)
    session.add(student)
session.commit()

# Datos de inscripciones
enrollment_data = [
    {'enrollment_date': '2023-01-10', 'approval': True, 'student_id': 1, 'course_id': 1},
    {'enrollment_date': '2023-01-15', 'approval': True, 'student_id': 2, 'course_id': 2},
    {'enrollment_date': '2023-02-20', 'approval': True, 'student_id': 3, 'course_id': 3},
    {'enrollment_date': '2023-02-25', 'approval': True, 'student_id': 4, 'course_id': 4},
    {'enrollment_date': '2023-03-10', 'approval': True, 'student_id': 5, 'course_id': 5}
]

for data in enrollment_data:
    enrollment = Enrollment(**data)
    session.add(enrollment)
session.commit()

# Datos de calificaciones
grade_data = [
    {'student_id': 1, 'course_id': 1, 'grade': 85.5},
    {'student_id': 2, 'course_id': 2, 'grade': 90.0},
    {'student_id': 3, 'course_id': 3, 'grade': 88.3},
    {'student_id': 4, 'course_id': 4, 'grade': 92.1},
    {'student_id': 5, 'course_id': 5, 'grade': 87.4}
]

for data in grade_data:
    grade = GradeRecord(**data)
    session.add(grade)
session.commit()

# Datos de asistencia
attendance_data = [
    {'student_id': 1, 'course_id': 1, 'attendance': True},
    {'student_id': 2, 'course_id': 2, 'attendance': True},
    {'student_id': 3, 'course_id': 3, 'attendance': True},
    {'student_id': 4, 'course_id': 4, 'attendance': True},
    {'student_id': 5, 'course_id': 5, 'attendance': False}
]

for data in attendance_data:
    attendance = AttendanceRecord(**data)
    session.add(attendance)
session.commit()

# Cerrar la sesión
session.close()