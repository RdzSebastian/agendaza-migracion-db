# pip install psycopg2  //adaptador de base de datos PostgreSQL para Python 
#
import psycopg2
import pandas as pd
from sqlalchemy import create_engine, exc

# Parámetros de conexión a la base de datos
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


    def __init__(self,db_parametros):
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


    def probar_consulta(self, query):
        if self.engine is None:
            self.realizar_conexion()
        try:
            resultado = pd.read_sql_query(query, self.engine)
            print("Resultado de la consulta:")
            print(resultado)
        except exc.SQLAlchemyError as e:
            print("Error al ejecutar la consulta:", e)



conexion_agendaza = ConexionBD(agendaza_db_parametros)
conexion_agendaza.probar_consulta('select * from usuario')


conexion_geservapp = ConexionBD(geservapp_db_parametros)
conexion_geservapp.probar_consulta('select * from usuario')






        


    

     
    

