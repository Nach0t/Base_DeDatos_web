# Web Database by NotaMaster

## Description:

* This web application manages a university system where you can search and analyze students, teachers, courses, grades and attendance. The application is built with Flask and uses SQLAlchemy to connect to a MySQL database.

## Characteristics:

- **Search for students, teachers and courses**: A dynamic search can be carried out by first name, last name or course in different entities of the database (students, teachers, courses, faculties, etc.).
  
- **Grade Record**: Student grades can be consulted, filtered by student or course name.

- **Performance analysis**: The `/analysis` path allows you to perform an analysis of the general performance of a student or in a specific course, displaying a distribution of the results in a graphical way (using the `perform_analysis` function).

- **Contact Form**: Includes a contact page managed through a blueprint (`contact_bp`).


### What You Need to Run the Project:

## Requirements
* Python 3.8 or higher
* Docker Desktop
* mysql:9.0.1

```bash
python -m pip install flask Flask-SQLAlchemy SQLAlchemy mysqlclient PyMySQL
```

## How to Run

### First Step: Open Docker Desktop

#### If you don't have MySQL installed, execute:
```bash
docker pull mysql:9.0.1
```

### Second Step: Start the Docker containers
```bash
cd ./docker/
docker compose up
```

### Third Step: Set up the database (use for example)
```bash
cd ./database/
python CreateDataBase.py
```

### Fourth Step: Run Flask
```bash
flask run
```

### Fifth Step: Open in your browser
```bash
http://127.0.0.1:5000/
```

### Project Members
* Ignacio Rehbein
* Claudio Diaz
* Vicente Quintanilla
