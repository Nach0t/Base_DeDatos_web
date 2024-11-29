from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, Float, Date
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

# Configuración de la base de datos
config = {
    'host': '172.19.0.2',
    'port': '3306',
    'database_name': 'universitydb',
    'user': 'root',
    'password': 'rootpass'
}

try:
    # Crear el motor de conexión
    engine = create_engine(f'mysql+pymysql://{config["user"]}:{config["password"]}@{config["host"]}:{config["port"]}', echo=False)
    with engine.connect() as conn:
        # Crear la base de datos si no existe
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {config['database_name']}"))
    # Reconectar al motor con la base de datos específica
    engine = create_engine(f'mysql+pymysql://{config["user"]}:{config["password"]}@{config["host"]}:{config["port"]}/{config["database_name"]}', echo=False)
    print("Conexión exitosa!")
except SQLAlchemyError as e:
    print(f"Error al conectar a la base de datos: {e}")

# Declaración de la base
Base = declarative_base()

# Modelos
class University(Base):
    __tablename__ = 'university'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    faculties = relationship('Faculty', back_populates='university', cascade='all, delete-orphan')

class Faculty(Base):
    __tablename__ = 'faculty'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    university_id = Column(Integer, ForeignKey('university.id'))
    university = relationship('University', back_populates='faculties')
    careers = relationship('Career', back_populates='faculty', cascade='all, delete-orphan')
    teachers = relationship('Teacher', back_populates='faculty', cascade='all, delete-orphan')

class Career(Base):
    __tablename__ = 'career'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    faculty_id = Column(Integer, ForeignKey('faculty.id'))
    faculty = relationship('Faculty', back_populates='careers')
    students = relationship('Student', back_populates='career', cascade='all, delete-orphan')
    courses = relationship('Course', back_populates='career', cascade='all, delete-orphan')

class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    faculty_id = Column(Integer, ForeignKey('faculty.id'))
    faculty = relationship('Faculty', back_populates='teachers')
    courses = relationship('Course', back_populates='teacher', cascade='all, delete-orphan')

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    career_id = Column(Integer, ForeignKey('career.id'))
    career = relationship('Career', back_populates='students')
    enrollments = relationship('Enrollment', back_populates='student', cascade='all, delete-orphan')
    grades = relationship('GradeRecord', back_populates='student', cascade='all, delete-orphan')
    attendances = relationship('AttendanceRecord', back_populates='student', cascade='all, delete-orphan')

class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    career_id = Column(Integer, ForeignKey('career.id'))
    teacher = relationship('Teacher', back_populates='courses')
    career = relationship('Career', back_populates='courses')
    evaluations = relationship('Evaluation', back_populates='course', cascade='all, delete-orphan')
    enrollments = relationship('Enrollment', back_populates='course', cascade='all, delete-orphan')
    attendances = relationship('AttendanceRecord', back_populates='course', cascade='all, delete-orphan')

    # Agregar estos dos campos a la clase Course
    weeks = Column(Integer, nullable=False, default=15)  # Número de semanas, con valor por defecto 15
    classes_per_week = Column(Integer, nullable=False, default=2)  # Número de clases por semana, con valor por defecto 2


class Enrollment(Base):
    __tablename__ = 'enrollment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    enrollment_date = Column(Date, nullable=False)
    approval = Column(Boolean, nullable=False)
    student_id = Column(Integer, ForeignKey('student.id'))
    course_id = Column(Integer, ForeignKey('course.id'))
    student = relationship('Student', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')
    average = Column(Float)  # Agregamos una columna para almacenar el promedio


class GradeRecord(Base):
    __tablename__ = 'grade_record'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    evaluation_id = Column(Integer, ForeignKey('evaluation.id'))
    grade = Column(Float)
    student = relationship('Student', back_populates='grades')
    evaluation = relationship('Evaluation', back_populates='grade_records')

class Evaluation(Base):
    __tablename__ = 'evaluation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('course.id'))
    name = Column(String(100), nullable=False)
    percentage = Column(Float, nullable=False)
    course = relationship('Course', back_populates='evaluations')
    grade_records = relationship('GradeRecord', back_populates='evaluation', cascade='all, delete-orphan')

class AttendanceRecord(Base):
    __tablename__ = 'attendance_record'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    course_id = Column(Integer, ForeignKey('course.id'))
    attendance = Column(Boolean, nullable=False)
    week = Column(Integer, nullable=False)
    class_number = Column(Integer)  # Asegúrate de que esta columna esté definida

    student = relationship('Student', back_populates='attendances')
    course = relationship('Course', back_populates='attendances')


try:
# Crear las tablas en la base de datos
    Base.metadata.create_all(engine)
    print("Tablas creadas con éxito.")
except: 
    print("Error en la creación de las tablas")
    
