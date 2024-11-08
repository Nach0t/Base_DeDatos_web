from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Boolean, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import text

# Configuración de la base de datos
config = {'host': 'localhost', 'database_name': 'universitydb', 'user': 'root', 'password': 'rootpass'}
engine = create_engine(f'mysql+pymysql://{config["user"]}:{config["password"]}@{config["host"]}/{config["database_name"]}', echo=False)
Base = declarative_base()

# Definición de modelos
class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    percentages = relationship('Percentage', back_populates='course')

class Percentage(Base):
    __tablename__ = 'percentage'
    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('course.id'))
    name = Column(String(100))
    percentage = Column(Float)
    course = relationship('Course', back_populates='percentages')

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Configuración de la sesión
Session = sessionmaker(bind=engine)

# Aplicación Flask
app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    session = Session()
    courses = session.query(Course).all()
    session.close()
    return render_template('index.html', courses=courses)

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course_name = request.form.get('course_name')
        eval_names = request.form.getlist('eval_name')
        eval_percentages = request.form.getlist('eval_percentage')
        eval_percentages = [float(p) for p in eval_percentages]
        
        if sum(eval_percentages) != 100:
            flash('El porcentaje total debe ser exactamente 100%. Por favor, ajuste los valores.')
            return redirect(url_for('add_course'))
        
        if course_name and eval_names and eval_percentages:
            session = Session()
            new_course = Course(name=course_name)
            session.add(new_course)
            session.commit()
            
            for name, percentage in zip(eval_names, eval_percentages):
                new_percentage = Percentage(name=name, percentage=percentage, course_id=new_course.id)
                session.add(new_percentage)
            session.commit()
            session.close()
            flash('Curso y evaluaciones agregados exitosamente')
            return redirect(url_for('index'))
    
    return render_template('add_course.html')

@app.route('/course/<int:course_id>')
def course_detail(course_id):
    session = Session()
    course = session.query(Course).filter_by(id=course_id).first()
    percentages = session.query(Percentage).filter_by(course_id=course_id).all()
    total_percentage = sum(p.percentage for p in percentages)
    session.close()
    return render_template('course_detail.html', course=course, percentages=percentages, total_percentage=total_percentage)

@app.route('/add_percentage/<int:course_id>', methods=['POST'])
def add_percentage(course_id):
    eval_name = request.form.get('eval_name')
    eval_percentage = float(request.form.get('eval_percentage'))
    session = Session()
    percentages = session.query(Percentage).filter_by(course_id=course_id).all()
    total_percentage = sum(p.percentage for p in percentages) + eval_percentage
    if total_percentage > 100:
        flash('El porcentaje total no puede exceder el 100%. Por favor, ajuste los valores.')
    else:
        new_percentage = Percentage(name=eval_name, percentage=eval_percentage, course_id=course_id)
        session.add(new_percentage)
        session.commit()
        flash('Evaluación agregada exitosamente')
    session.close()
    return redirect(url_for('course_detail', course_id=course_id))

@app.route('/delete_percentage/<int:percentage_id>/<int:course_id>', methods=['POST'])
def delete_percentage(percentage_id, course_id):
    session = Session()
    percentage = session.query(Percentage).filter_by(id=percentage_id).first()
    if percentage:
        session.delete(percentage)
        session.commit()
        flash('Evaluación eliminada exitosamente')
    session.close()
    return redirect(url_for('course_detail', course_id=course_id))

@app.route('/delete_course/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    session = Session()
    course = session.query(Course).filter_by(id=course_id).first()
    if course:
        session.delete(course)
        session.commit()
        flash('Curso eliminado exitosamente')
    session.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
