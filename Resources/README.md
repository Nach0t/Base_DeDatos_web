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