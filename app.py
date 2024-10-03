from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from database import University, Faculty, Career, Teacher, Student, Course, Enrollment, GradeRecord, AttendanceRecord
from sqlalchemy import create_engine

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:rootpass@localhost:3306/universitydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with Flask
db = SQLAlchemy(app)

# Set up SQLAlchemy engine and session
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI']) 
Session = sessionmaker(bind=engine)
session = Session()

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/application', methods=['GET'])
def application():
    query = request.args.get('query', '')

    results = {
        'students': [],
        'teachers': [],
        'courses': [],
        'grades': [],
        'faculty_students': [],
        'faculty_teachers': []
    }

    if query:
        # Search students by first or last name
        results['students'] = session.query(Student).filter(
            (Student.first_name.like(f'%{query}%')) | (Student.last_name.like(f'%{query}%'))
        ).all()

        # Search teachers by first or last name
        results['teachers'] = session.query(Teacher).filter(
            (Teacher.first_name.like(f'%{query}%')) | (Teacher.last_name.like(f'%{query}%'))
        ).all()

        # Search courses by name
        results['courses'] = session.query(Course).filter(
            Course.name.like(f'%{query}%')
        ).all()

        # Search grades based on student name, course name, or grade
        results['grades'] = session.query(
            Student.first_name, Student.last_name, Course.name, GradeRecord.grade
        ).join(GradeRecord, Student.id == GradeRecord.student_id).join(Course, GradeRecord.course_id == Course.id).filter(
            (Student.first_name.like(f'%{query}%')) |
            (Student.last_name.like(f'%{query}%')) |
            (Course.name.like(f'%{query}%'))
        ).all()

        # Search faculties by name and show associated students and teachers
        faculties = session.query(Faculty).filter(
            Faculty.name.like(f'%{query}%')
        ).all()

        for faculty in faculties:
            # Get all students in the faculty
            faculty_students = session.query(Student).join(Career).filter(Career.faculty_id == faculty.id).all()
            results['faculty_students'].extend(faculty_students)

            # Get all teachers in the faculty
            faculty_teachers = session.query(Teacher).join(Career).filter(Career.faculty_id == faculty.id).all()
            results['faculty_teachers'].extend(faculty_teachers)

    return render_template('application.html', results=results, query=query)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    # Receive form data
    first_name = request.form.get('name')
    last_name = request.form.get('lastname')
    email = request.form.get('email')
    phone = request.form.get('phone')
    reason = request.form.get('reason')
    subject = request.form.get('subject')
    message = request.form.get('message')
    recipient = request.form.get('email-select')

    # Here you can process the data, e.g., send an email or save to the database

    return "Form submitted successfully!"

# Route for the dynamic search functionality in research.js
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')

    results = {
        'students': [],
        'teachers': [],
        'courses': [],
        'grades': [],
        'faculty_students': [],
        'faculty_teachers': []
    }

    if query:
        # Search in the students table
        results['students'] = session.query(Student).filter(
            (Student.first_name.like(f'%{query}%')) | (Student.last_name.like(f'%{query}%'))
        ).all()

        # Search in the teachers table
        results['teachers'] = session.query(Teacher).filter(
            (Teacher.first_name.like(f'%{query}%')) | (Teacher.last_name.like(f'%{query}%'))
        ).all()

        # Search in the courses table
        results['courses'] = session.query(Course).filter(
            Course.name.like(f'%{query}%')
        ).all()

        # Search in the grades table
        results['grades'] = session.query(
            Student.first_name, Student.last_name, Course.name, GradeRecord.grade
        ).join(GradeRecord, Student.id == GradeRecord.student_id).join(Course, Course.id == GradeRecord.course_id).filter(
            (Student.first_name.like(f'%{query}%')) | 
            (Student.last_name.like(f'%{query}%')) | 
            (Course.name.like(f'%{query}%'))
        ).all()

        # Search faculties by name and show associated students and teachers
        faculties = session.query(Faculty).filter(
            Faculty.name.like(f'%{query}%')
        ).all()

        for faculty in faculties:
            # Get all students in the faculty
            faculty_students = session.query(Student).join(Career).filter(Career.faculty_id == faculty.id).all()
            results['faculty_students'].extend(faculty_students)

            # Get all teachers in the faculty
            faculty_teachers = session.query(Teacher).join(Career).filter(Career.faculty_id == faculty.id).all()
            results['faculty_teachers'].extend(faculty_teachers)

    return render_template('application.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
