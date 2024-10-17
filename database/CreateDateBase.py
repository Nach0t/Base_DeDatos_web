from DataBase import *  # Mala práctica de programación, pero se hace para simplificar el código

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

# Datos de profesores (algunos compartidos entre facultades)
teacher_data = [
    {'first_name': 'Carlos', 'last_name': 'Garcia', 'faculty_id': 1},
    {'first_name': 'Laura', 'last_name': 'Diaz', 'faculty_id': 2},
    {'first_name': 'Fernando', 'last_name': 'Gomez', 'faculty_id': 3},
    {'first_name': 'Clara', 'last_name': 'Sanchez', 'faculty_id': 4},
    {'first_name': 'Carlos', 'last_name': 'Garcia', 'faculty_id': 2},  # Mismo profesor en dos facultades
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

# Datos de inscripciones actualizados (un mismo estudiante en varios cursos)
enrollment_data = [
    {'enrollment_date': '2023-01-10', 'approval': True, 'student_id': 1, 'course_id': 1},  # José en Data Structures
    {'enrollment_date': '2023-01-12', 'approval': True, 'student_id': 1, 'course_id': 2},  # José en Mechanical Design
    {'enrollment_date': '2023-01-15', 'approval': True, 'student_id': 2, 'course_id': 2},  # Luisa en Mechanical Design
    {'enrollment_date': '2023-02-20', 'approval': True, 'student_id': 3, 'course_id': 3},  # Diego en Corporate Strategy
    {'enrollment_date': '2023-02-25', 'approval': True, 'student_id': 4, 'course_id': 4},  # Ana en Financial Analysis
    {'enrollment_date': '2023-03-10', 'approval': True, 'student_id': 5, 'course_id': 5},  # Lucia en Advanced Painting
    {'enrollment_date': '2023-03-15', 'approval': True, 'student_id': 1, 'course_id': 3},  # José en Corporate Strategy
    {'enrollment_date': '2023-03-20', 'approval': True, 'student_id': 2, 'course_id': 4},  # Luisa en Financial Analysis
    {'enrollment_date': '2023-03-25', 'approval': True, 'student_id': 5, 'course_id': 1}   # Lucia en Data Structures
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
    {'student_id': 5, 'course_id': 5, 'grade': 87.4},
    {'student_id': 1, 'course_id': 2, 'grade': 82.0},  # José en Mechanical Design
    {'student_id': 1, 'course_id': 3, 'grade': 89.0},  # José en Corporate Strategy
    {'student_id': 2, 'course_id': 4, 'grade': 93.0},  # Luisa en Financial Analysis
    {'student_id': 5, 'course_id': 1, 'grade': 91.5}   # Lucia en Data Structures
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
    {'student_id': 5, 'course_id': 5, 'attendance': False},
    {'student_id': 1, 'course_id': 2, 'attendance': True},  # José en Mechanical Design
    {'student_id': 1, 'course_id': 3, 'attendance': True},  # José en Corporate Strategy
    {'student_id': 2, 'course_id': 4, 'attendance': True},  # Luisa en Financial Analysis
    {'student_id': 5, 'course_id': 1, 'attendance': True}   # Lucia en Data Structures
]

for data in attendance_data:
    attendance = AttendanceRecord(**data)
    session.add(attendance)
session.commit()

# Cerrar la sesión
session.close()
