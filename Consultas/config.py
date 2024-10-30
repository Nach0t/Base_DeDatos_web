from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

config = {
    'host': 'mysql',  # Nombre del servicio en docker-compose.yml
    'database_name': 'universitydb',
    'user': 'root',
    'password': 'rootpass'
}
# Crear el motor de conexión a la base de datos MySQL usando los datos de configuración
engine = create_engine(
    f'mysql+pymysql://{config["user"]}:{config["password"]}@{config["host"]}/{config["database_name"]}',
    echo=False
)

# Configurar la sesión
Session = sessionmaker(bind=engine)
