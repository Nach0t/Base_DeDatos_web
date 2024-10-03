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
  +nota: float
}

entity "Registro_asistencias" {
  +ID: int
  +id_estudiante: int
  +id_curso: int
  +asistencia: boolean
}
entity "Inscripcion" {
  +ID: int
  +fecha_inscripcion: string
  +aprobacion: boolean   
}


' Relación entre Universidad y Facultad (1 a N)
Universidad --o{ Facultad : tiene

' Relación entre Facultad y Profesor (1 a N)
Facultad --o{ Profesor : tiene

' Relación entre Facultad y Carrera (1 a N)
Facultad --o{ Carrera : tiene

' Relación entre Carrera y Estudiante (1 a N)
Carrera --o{ Estudiante : tiene

' Relación entre Profesor y Curso (1 a N)
Profesor --o{ Curso : dicta

' Relación entre Curso y Inscripcion (1 a N)
Curso --o{ Inscripcion : tiene

' Relación entre Estudiante y Inscripcion (1 a N)
Estudiante --o{ Inscripcion : tiene

' Relacion entre Inscripcion y Registro_notas (1 a N)
Inscripcion --o{ Registro_notas : tiene

' Relacion entre Inscripcion y Registro_asistencias (1 a N)
Inscripcion --o{ Registro_asistencias : tiene


@enduml
