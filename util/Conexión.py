# pip install psycopg2  //adaptador de base de datos PostgreSQL para Python 
#
import psycopg2
import pandas as pd
from sqlalchemy import create_engine, exc


class ConexionBD:
    db_parametros = None
    engine = None

    def __init__(self, db_parametros):
        self.db_parametros = db_parametros

    def construir_url(self):
        return f"postgresql://{self.db_parametros['user']}:{self.db_parametros['password']}@{self.db_parametros['host']}:{self.db_parametros['port']}/{self.db_parametros['dbname']}"

    def realizar_conexion(self):
        try:
            url = self.construir_url()
            self.engine = create_engine(url)

            print(f"conexion para la base {self.db_parametros['dbname']} fue realizada correctamente")
        except exc.SQLAlchemyError as e:
            print("Error al conectar a la base de datos:", e)

    def realizar_consulta(self, query):
        if self.engine is None:
            self.realizar_conexion()
        try:
            resultado = pd.read_sql_query(query, self.engine)
            return resultado
        except exc.SQLAlchemyError as e:
            print("Error al ejecutar la consulta:", e)

    def visualizar_consulta(self, query):
        print(self.realizar_consulta(query))
