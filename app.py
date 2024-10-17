from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from database.DataBase import University, Faculty, Career, Teacher, Student, Course, Enrollment, GradeRecord, AttendanceRecord
from sqlalchemy import create_engine
from function.analysis import perform_analysis
from function.contact import *
from function.application import application_view  
from function.search import search_blueprint

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

@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    query = request.args.get('query', '')  # Obtener el término de búsqueda desde el formulario
    analysis_results = perform_analysis(query)  # Llamar a la función para realizar el análisis
    return render_template('analysis.html', analysis_results=analysis_results, query=query)

@app.route('/contact')
def contact():
    return render_template('contact.html')

app.register_blueprint(contact_bp)

@app.route('/application', methods=['GET'])
def application():
    return application_view() 

# Route for the dynamic search functionality in research.js
app.register_blueprint(search_blueprint)

if __name__ == '__main__':
    app.run(debug=True)