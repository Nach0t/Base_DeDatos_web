### Project Structure

```plaintext
/Root
├── resources/
│   ├── README.MD (Project Structure)
│   └── GanttChart.pdf
│
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
│   ├── search.py
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
│   │   ├── README.md (DiagramER in uml)
│   │   └── PhotoER.png
│   │
│   ├── JSON /
│   │   ├── mails/
│   │   │    └── contact_data.json
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