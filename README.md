# Web Database

### What You Need to Run the Project:

### Project Structure

```plaintext
/Root
│
├── database/  
│   ├── CreateDataBase.py
│   └── DataBase.py
│
├── templates/
│   ├── index.html
│   ├── application.html 
│   ├── contact.html
│   └── about.html
│
├── docker/
│   ├── mysql-data/
│   └── compose.yml
│
├── function
│   ├── analysis.py
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
│   │   └── 
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
  
```plaintext
  python -m pip install flask Flask-SQLAlchemy SQLAlchemy mysqlclient PyMySQL
```
## How to Run

```plaintext
cd path/to/database/ python CreateDataBase.py
```

### Members
* Ignacio Rehbein
* Claudio Diaz
* Vicente Quintanilla
