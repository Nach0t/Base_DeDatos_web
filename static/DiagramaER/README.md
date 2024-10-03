The UML code of DiagrammER

```plaintext

@startuml

entity "University" {
  +ID: int
  +name: string
}

entity "Faculty" {
  +ID: int
  +name: string
}

entity "Degree Program" {
  +ID: int
  +name: string
}

entity "Professor" {
  +ID: int
  +firstName: string
  +lastName: string
}

entity "Student" {
  +ID: int
  +firstName: string
  +lastName: string
}

entity "Course" {
  +ID: int
  +name: string
}

entity "Grades_Record" {
  +ID: int
  +student_id: int
  +course_id: int
  +grade: float
}

entity "Attendance_Record" {
  +ID: int
  +student_id: int
  +course_id: int
  +attendance: boolean
}

entity "Enrollment" {
  +ID: int
  +enrollment_date: string
  +approval: boolean   
}


' Relationship between University and Faculty (1 to N)
University --o{ Faculty : has

' Relationship between Faculty and Professor (1 to N)
Faculty --o{ Professor : has

' Relationship between Faculty and Degree Program (1 to N)
Faculty --o{ Degree Program : has

' Relationship between Degree Program and Student (1 to N)
Degree Program --o{ Student : has

' Relationship between Professor and Course (1 to N)
Professor --o{ Course : teaches

' Relationship between Course and Enrollment (1 to N)
Course --o{ Enrollment : has

' Relationship between Student and Enrollment (1 to N)
Student --o{ Enrollment : has

' Relationship between Enrollment and Grades_Record (1 to N)
Enrollment --o{ Grades_Record : has

' Relationship between Enrollment and Attendance_Record (1 to N)
Enrollment --o{ Attendance_Record : has

@enduml
```
