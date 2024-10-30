from sqlalchemy import create_engine
from sqlalchemy import text

config = {'host': 'localhost', 'database_name': 'universitydb', 'user': 'root', 'password': 'rootpass'}

engine = create_engine(f'mysql+pymysql://{config["user"]}:{config["password"]}@{config["host"]}/{config["database_name"]}', echo=False)

def consultar_notas(student_id):
    try:
        with engine.connect() as conn:
            res = conn.execute(text(f'SELECT grade FROM grade_record WHERE student_id = :student_id'), {'student_id':student_id})
            print(res.all())
        pass
    except Exception as e:
        print(f'Error in query 1: {e}')

def consultar_asistencias(student_id):
    try:
        with engine.connect() as conn:
            res = conn.execute(text(f'SELECT attendance FROM attendance_record WHERE student_id = :student_id'), {'student_id':student_id})
            print(res.all())
        pass
    except Exception as e:
        print(f'Error in query 2: {e}')

def insertar_nota(student_id,percentage_id,grade):
    try:
        with engine.connect() as conn:
            conn.execute(text(f'INSERT INTO grade_record(student_id, percentage_id, grade) VALUES (:student_id,:percentage_id,:grade);'),{'student_id':student_id,'percentage_id':percentage_id,'grade':grade})
            conn.execute(text(f'COMMIT;'))
        pass
    except Exception as e:
        print(f'Error in query 3: {e}')

def insertar_notas_curso(course_id,testname,percentage):
    try:
        with engine.connect() as conn:
            conn.execute(text(f'INSERT INTO percentage(course_id, name, percentage) VALUES (:course_id, :testname, :percentage);'),{'course_id':course_id,'testname':testname,'percentage':percentage})
            conn.execute(text(f'COMMIT;'))
        pass
    except Exception as e:
        print(f'Error in query 4: {e}')

def insertar_asistencia(student_id,course_id,attendance):
    try:
        with engine.connect() as conn:
            conn.execute(text(f'INSERT INTO attendance_record(student_id, course_id, attendance) VALUES (:student_id,:course_id,:attendance);'),{'student_id':student_id,'course_id':course_id,'attendance':attendance})
            conn.execute(text(f'COMMIT;'))
        pass
    except Exception as e:
        print(f'Error in query 3: {e}')

if __name__ == '__main__':
    consultar_notas(1)
    consultar_asistencias(1)
    insertar_asistencia(1,2,0)
