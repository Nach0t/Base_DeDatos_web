# Web Database

### What You Need to Run the Project:

### Project Structure

```plaintext
/Root
├── resources/
│   └── GanttChart.pdf
│
├── database/  
│   ├── CreateDataBase.py
│   └── DataBase.py
│
├── templates/
│   ├── index.html
│   ├── application.html 
│   ├── contact.html
│   ├── analysis.html
│   └── about.html
│
├── docker/
│   ├── mysql-data/
│   └── compose.yml
│
├── function
│   ├── analysis.py
│   ├── contact.py
│   └── application.py
│
│
├── static/
│   │
│   ├── CSS/
│   │   ├── styles.css
│   │   └── normalize.css
│   │
│   ├── DiagramaER/
│   │   ├── DiagramaER.md
│   │   └── PhotoER.png
│   │
│   ├── JSON /
│   │   ├── mails/
│   │   │    └──
│   │   │
│   │   └── language/
│   │          ├── Index/
│   │          │     ├── en.json
│   │          │     └── es.json
│   │          │
│   │   
│   ├── JAVASCRIPT/
│   │   ├── translation.js
│   │   └── theme.js
│   │
│   └── PICTURE/
│       ├── symbols/
│       │   ├── sun.png
│       │   ├── mon.png
│       │   ├── HTML.png
│       │   └── CSS.png
│       │
│       └── icons/
│           ├── favicon.ico
│           └── log.png
│
└── app.py
```

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
cd path/to/the/file/zdocker/
docker compose up
```

### Third Step: Set up the database
```bash
cd path/to/the/file/database/
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
* Claudio
