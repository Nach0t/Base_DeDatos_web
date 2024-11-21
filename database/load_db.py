from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DECIMAL, Date, Boolean, Float
from sqlalchemy import text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError

config = {'host': 'localhost','port': '3306', 'database_name': 'universitydb', 'user': 'root', 'password': 'rootpass'}


try:
    engine = create_engine(f'mysql+pymysql://{config["user"]}:{config["password"]}@{config["host"]}:{config["port"]}', echo=False)
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {config["database_name"]}"))
    engine = create_engine(f'mysql+pymysql://{config["user"]}:{config["password"]}@{config["host"]}:{config["port"]}/{config["database_name"]}', echo=False)
    print("Conexión exitosa!")
except SQLAlchemyError as e:
    print(f"Error al conectar a la base de datos: {e}")

Base = declarative_base()

class University(Base):
    __tablename__= 'university'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    faculties = relationship('Faculty', back_populates='university')

class Faculty(Base):
    __tablename__ = 'faculty'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    university_id = Column(Integer, ForeignKey('university.id'))
    university = relationship('University', back_populates='faculties')
    careers = relationship('Career', back_populates='faculty')
    teachers = relationship('Teacher', back_populates='faculty')

class Career(Base):
    __tablename__ = 'career'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    faculty_id = Column(Integer, ForeignKey('faculty.id'))
    faculty = relationship('Faculty', back_populates='careers')
    students = relationship('Student', back_populates='career')
    courses = relationship('Course', back_populates='career')

class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    mother_lastname = Column(String(100), nullable=False)
    father_lastname = Column(String(100), nullable=False)
    faculty_id = Column(Integer, ForeignKey('faculty.id'))
    faculty = relationship('Faculty', back_populates='teachers')
    courses = relationship('Course', back_populates='teacher')

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    career_id = Column(Integer, ForeignKey('career.id'))
    career = relationship('Career', back_populates='students')
    enrollments = relationship('Enrollment', back_populates='student')
    grades = relationship('GradeRecord', back_populates='student')
    attendances = relationship('AttendanceRecord', back_populates='student')

class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    career_id = Column(Integer, ForeignKey('career.id'))
    teacher = relationship('Teacher', back_populates='courses')
    career = relationship('Career', back_populates='courses')
    evaluations = relationship('Evaluation', back_populates='course')
    enrollments = relationship('Enrollment', back_populates='course')
    attendances = relationship('AttendanceRecord', back_populates='course')

class Enrollment(Base):
    __tablename__ = 'enrollment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    enrollment_date = Column(Date, nullable=False)
    approval = Column(Boolean, nullable=False)
    student_id = Column(Integer, ForeignKey('student.id'))
    course_id = Column(Integer, ForeignKey('course.id'))
    student = relationship('Student', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')

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
    name = Column(String(100))
    percentage = Column(Float)
    course = relationship('Course', back_populates='evaluations')
    grade_records = relationship('GradeRecord', back_populates='evaluation')

class AttendanceRecord(Base):
    __tablename__ = 'attendance_record'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    course_id = Column(Integer, ForeignKey('course.id'))
    attendance = Column(Boolean)
    week = Column(Integer)
    student = relationship('Student', back_populates='attendances')
    course = relationship('Course', back_populates='attendances')

# Create the tables in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Commit the changes to the database
session.commit()

# Close the session
session.close()