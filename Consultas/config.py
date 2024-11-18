<<<<<<< HEAD
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
=======
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
>>>>>>> 8a021f5ad76212057002338ff95c18bd030e2ee5
