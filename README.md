# Web Database by NotaMaster

## Project Overview:

* A web application designed to manage and administer university courses. It allows you to assign professors, enroll students, register evaluations, monitor attendance, and calculate student averages.

## Main Features:

- **Course Management**:
  * Add new courses.
  * Assign professors to courses.
  * Enroll students in courses.
  
- **Evaluation and Grades**:
  * Register evaluations with assigned percentages.
  * Assign grades to students.
  * Automatically calculate student averages.

- **Attendance**:
  * Record student attendance.
    
- **System entities**:
   * University, faculties, careers, courses, students, and professors.

### Technologies Used
* **Backend**: Flask (python)
* **Database**: SQLAlchemy
* **Frontend**: HTML, CSS, JavaScript
 
### What You Need to Run the Project:

## Requirements
* Python 3.8 or higher
* Docker Desktop
* mysql:9.0.1
  
Install the required dependencies:
```bash
python -m pip install flask Flask-SQLAlchemy SQLAlchemy mysqlclient PyMySQL pandas
```

# How to Run the proyect

## If you use Windows

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
python load.py
```


### fourth Step: Set up the database (use for example)
```bash
cd ./database/
python insert.py
```

### fifth Step: Run Flask
```bash
flask run
```

### sixth Step: Open in your browser
```bash
http://127.0.0.1:5000/
```

### Using the aplication
Navigate through the following sections in the web application:


# If you use a azure:

### First Step: create enviaroments
```bash
cd enviroments/
```

```bash
source my_env/bin/activate
```

### Second Step: clone the proyect
```bash
cd gitHub/Base_DeDatos_web/
```

### Trirh Step: Open Docker Desktop

#### If you don't have MySQL installed, execute:
```bash
docker pull mysql:9.0.1
```

### Fouth Step: Start the Docker containers
```bash
cd ./docker/
docker compose up
```

### fifth Step: Set up the database (use for example)
```bash
cd ./database/
python load.py
```


### sixth Step: Set up the database (use for example)
```bash
cd ./database/
python insert.py
```

### seventh Step: Set up the database (use for example)
```bash
flask run --host=0.0.0.0 --port=5000
```


### Project Members
* Ignacio Rehbein
* Claudio Diaz
* Vicente Quintanilla
