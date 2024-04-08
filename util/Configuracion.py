from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from Conexión import ConexionBD
from repositorio.Repository import UsuarioLegacyRepository

agendaza_db_parametros = {
    'dbname': 'agendaza',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432'
}
geservapp_db_parametros = {
    'dbname': 'geserveapp',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5433'
}


class Configuracion:
    def __init__(self):
        self.conexion_agendaza = None
        self.conexion_geserveapp = None
        self.usuario_elegacy_repositorio = None
        self.base = None

    def inicializar(self):
        self.base = declarative_base()
        self.conexion_agendaza = ConexionBD(agendaza_db_parametros)
        self.conexion_geserveapp = ConexionBD(geservapp_db_parametros)
        engine_geservapp = self.conexion_geserveapp.engine
        self.usuario_elegacy_repositorio = UsuarioLegacyRepository(sessionmaker(engine_geservapp))
