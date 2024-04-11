# pip install psycopg2  //adaptador de base de datos PostgreSQL para Python 
#
import psycopg2
import pandas as pd
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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


class ConexionBD:
    db_parametros = None
    engine = None
    Session = None
    Base = None

    def __init__(self, db_parametros):
        self.db_parametros = db_parametros

    def construir_url(self):
        return f"postgresql://{self.db_parametros['user']}:{self.db_parametros['password']}@{self.db_parametros['host']}:{self.db_parametros['port']}/{self.db_parametros['dbname']}"

    def realizar_conexion(self):
        try:
            url = self.construir_url()
            self.engine = create_engine(url)
            self.Session = sessionmaker(bind=self.engine)
            print(f"Conexión a la base de datos {self.db_parametros['dbname']} establecida correctamente")
            self.Base = declarative_base()
            self.Base.metadata.create_all(self.engine, checkfirst=True)
        except exc.SQLAlchemyError as e:
            print("Error al conectar a la base de datos:", e)

    def cerrar_conexion(self):
        if self.engine is not None:
            self.engine.dispose()
            print("Conexión cerrada correctamente")

    def realizar_consulta(self, query):
        if self.engine is None:
            self.realizar_conexion()
        try:
            with self.Session() as session:
                resultado = pd.read_sql_query(query, session.bind)
                return resultado
        except exc.SQLAlchemyError as e:
            print("Error al ejecutar la consulta:", e)
            return None

    def visualizar_consulta(self, query):
        print(self.realizar_consulta(query))


conexionAgendaza = ConexionBD(agendaza_db_parametros)
conexionGeserveApp = ConexionBD(geservapp_db_parametros)

