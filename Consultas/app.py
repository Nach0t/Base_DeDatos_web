from flask import Flask, request, render_template, redirect, url_for, flash, Response
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from models import Session, Course, Student, Percentage, GradeRecord, Enrollment, AttendanceRecord
from datetime import date
import csv

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necessary to display flash messages
session = Session()

@app.route('/')
def index():
    return render_template('course.html')

@app.route('/attendance')
def attendance():
    return render_template('attendance.html')

@app.route('/add_course', methods=['POST'])
def add_course():
    name = request.form['name']
    try:
        existing_course = session.query(Course).filter_by(name=name).first()
        if existing_course:
            flash("Course already exists. No new record added.")
        else:
            new_course = Course(name=name)
            session.add(new_course)
            session.commit()
            flash("Course added successfully.")
        return redirect(url_for('index'))
    except Exception as e:
        session.rollback()
        flash(f"Error adding course: {e}")
        return redirect(url_for('index'))

@app.route('/add_student', methods=['POST'])
def add_student():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    try:
        existing_student = session.query(Student).filter_by(first_name=first_name, last_name=last_name).first()
        if existing_student:
            flash("Student already exists in the database.")
        else:
            new_student = Student(first_name=first_name, last_name=last_name)
            session.add(new_student)
            session.commit()
            flash("Student added successfully.")
        return redirect(url_for('index'))
    except Exception as e:
        session.rollback()
        flash(f"Error adding student: {e}")
        return redirect(url_for('index'))

@app.route('/enroll_student', methods=['POST'])
def enroll_student():
    student_id = request.form['student_id']
    course_id = request.form['course_id']
    enrollment_date = date.today()
    try:
        # Check if the student is already enrolled in the course
        existing_enrollment = session.query(Enrollment).filter_by(student_id=student_id, course_id=course_id).first()
        if existing_enrollment:
            flash("Student is already enrolled in this course.")
        else:
            new_enrollment = Enrollment(student_id=student_id, course_id=course_id, enrollment_date=enrollment_date, approval=False)
            session.add(new_enrollment)
            session.commit()
            flash("Student enrolled in the course successfully.")
        return redirect(url_for('index'))
    except Exception as e:
        session.rollback()
        flash(f"Error enrolling student: {e}")
        return redirect(url_for('index'))

@app.route('/assign_percentage', methods=['POST'])
def assign_percentage():
    course_id = request.form['course_id']
    test_name = request.form['testname']
    percentage = request.form['percentage']
    try:
        existing_percentage = session.query(Percentage).filter_by(course_id=course_id, name=test_name).first()
        if existing_percentage:
            existing_percentage.percentage = percentage  # Update percentage if it already exists
            flash("Test percentage updated successfully.")
        else:
            new_percentage = Percentage(course_id=course_id, name=test_name, percentage=percentage)
            session.add(new_percentage)
            flash("Percentage assigned successfully.")
        session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        session.rollback()
        flash(f"Error assigning percentage: {e}")
        return redirect(url_for('index'))

@app.route('/add_grade', methods=['POST'])
def add_grade():
    student_id = request.form['student_id']
    percentage_id = request.form['percentage_id']
    grade = request.form['grade']
    try:
        new_grade = GradeRecord(student_id=student_id, percentage_id=percentage_id, grade=grade)
        session.add(new_grade)
        session.commit()
        flash("Grade added successfully.")
        return redirect(url_for('index'))
    except Exception as e:
        session.rollback()
        flash(f"Error adding grade: {e}")
        return redirect(url_for('index'))

@app.route('/edit_grade', methods=['POST'])
def edit_grade():
    student_id = request.form['student_id']
    percentage_id = request.form['percentage_id']
    new_grade = request.form['new_grade']
    try:
        existing_grade = session.query(GradeRecord).filter_by(student_id=student_id, percentage_id=percentage_id).first()
        if existing_grade:
            existing_grade.grade = new_grade  # Update the grade if it already exists
            flash("Grade updated successfully.")
        else:
            flash("Specified grade does not exist.")
        session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        session.rollback()
        flash(f"Error editing grade: {e}")
        return redirect(url_for('index'))

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    course_id = request.form['course_id']
    student_id = request.form['student_id']
    attended = request.form['attendance'] == 'true'
    try:
        # Register student attendance
        new_attendance = AttendanceRecord(student_id=student_id, course_id=course_id, attendance=attended)
        session.add(new_attendance)
        session.commit()
        flash("Attendance recorded successfully.")
    except Exception as e:
        session.rollback()
        flash(f"Error recording attendance: {e}")
    return redirect(url_for('attendance'))

@app.route('/export_grades', methods=['GET'])
def export_grades():
    course_id = request.args.get('course_id')
    try:
        # Query student grades in the course
        grades = (
            session.query(Student.first_name, Student.last_name, Percentage.name, Percentage.percentage, GradeRecord.grade)
            .join(Enrollment, Student.id == Enrollment.student_id)
            .join(Course, Course.id == Enrollment.course_id)
            .join(GradeRecord, Student.id == GradeRecord.student_id)
            .join(Percentage, Percentage.id == GradeRecord.percentage_id)
            .filter(Course.id == course_id)
            .all()
        )

        # Create CSV file
        def generate():
            data = [('First Name', 'Last Name', 'Test', 'Percentage', 'Grade')]
            data += [(g.first_name, g.last_name, g.name, g.percentage, g.grade) for g in grades]

            output = []
            for row in data:
                output.append(','.join(f'"{str(value)}"' for value in row))
            return '\n'.join(output) + '\n'

        return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=grades.csv"})
    except Exception as e:
        flash(f"Error exporting grades: {e}")
        return redirect(url_for('attendance'))

if __name__ == '__main__':
    app.run(debug=True)
