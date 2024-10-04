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