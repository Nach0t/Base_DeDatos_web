```plaintext
@startuml

entity "Universidad" {
  +ID: int
  +nombre: string
}

entity "Facultad" {
  +ID: int
  +nombre: string
}

entity "Carrera" {
  +ID: int
  +nombre: string
}

entity "Profesor" {
  +ID: int
  +nombre: string
  +apellido: string
}

entity "Estudiante" {
  +ID: int
  +nombre: string
  +apellido: string
}

entity "Curso" {
  +ID: int
  +nombre: string
}

entity "Registro_notas" {
  +ID: int
  +id_estudiante: int
  +id_curso: int
  +nota: float[]
}

entity "Registro_asistencias" {
  +ID: int
  +id_estudiante: int
  +id_curso: int
  +asistencia: boolean[]
}

' Relación entre Universidad y Facultad (1 a N)
Universidad --o{ Facultad : tiene

' Relación entre Facultad y Profesor (1 a N)
Facultad --o{ Profesor : tiene

' Relación entre Facultad y Carrera (1 a N)
Facultad --o{ Carrera : tiene

' Relación entre Carrera y Estudiante (1 a N)
Carrera --o{ Estudiante : tiene

' Relación entre Estudiante y Curso (N a N)
Estudiante }o--o{ Curso : Inscribe

' Relación entre Profesor y Curso (1 a N)
Profesor --o{ Curso : dicta

' Relación entre Curso y Registro_notas (1 a N)
Curso --o{ Registro_notas : tiene

' Relación entre Estudiante y Registro_notas (1 a N)
Estudiante --o{ Registro_notas : tiene

' Relación entre Curso y Registro_asistencias (1 a N)
Curso --o{ Registro_asistencias : tiene

' Relación entre Estudiante y Registro_asistencias (1 a N)
Estudiante ||--o{ Registro_asistencias : tiene

@enduml
```
