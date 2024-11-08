from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Boolean, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import text

# Configuración de la base de datos
config = {'host': 'localhost', 'database_name': 'universitydb', 'user': 'root', 'password': 'rootpass'}
engine = create_engine(f'mysql+pymysql://{config["user"]}:{config["password"]}@{config["host"]}', echo=False)

# Crear la base de datos si no existe
with engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {config['database_name']}"))

# Conectar a la base de datos
engine = create_engine(f'mysql+pymysql://{config["user"]}:{config["password"]}@{config["host"]}/{config["database_name"]}', echo=False)
Base = declarative_base()

# Definición de modelos
class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    percentages = relationship('Percentage', back_populates='course')
    enrollments = relationship('Enrollment', back_populates='course')
    attendances = relationship('AttendanceRecord', back_populates='course')

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    enrollments = relationship('Enrollment', back_populates='student')
    grades = relationship('GradeRecord', back_populates='student')
    attendances = relationship('AttendanceRecord', back_populates='student')

class Percentage(Base):
    __tablename__ = 'percentage'
    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('course.id'))
    name = Column(String(100))
    percentage = Column(Float)
    course = relationship('Course', back_populates='percentages')
    grade_records = relationship('GradeRecord', back_populates='percentage')

class GradeRecord(Base):
    __tablename__ = 'grade_record'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    percentage_id = Column(Integer, ForeignKey('percentage.id'))
    grade = Column(Float)
    student = relationship('Student', back_populates='grades')
    percentage = relationship('Percentage', back_populates='grade_records')

class Enrollment(Base):
    __tablename__ = 'enrollment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    enrollment_date = Column(Date, nullable=False)
    approval = Column(Boolean, nullable=False)
    student_id = Column(Integer, ForeignKey('student.id'))
    course_id = Column(Integer, ForeignKey('course.id'))
    student = relationship('Student', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')

class AttendanceRecord(Base):
    __tablename__ = 'attendance_record'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    course_id = Column(Integer, ForeignKey('course.id'))
    week = Column(Integer, nullable=False)  # Se añadió la columna week para identificar la semana
    attendance = Column(Boolean)
    student = relationship('Student', back_populates='attendances')
    course = relationship('Course', back_populates='attendances')

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Configuración de la sesión
Session = sessionmaker(bind=engine)
