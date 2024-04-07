# pip install psycopg2  //adaptador de base de datos PostgreSQL para Python 
#
import psycopg2
import pandas as pd


# Parámetros de conexión a la base de datos
agendaza_db_parametros = {
    'dbname': 'agendaza',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432'  
}


geservapp_db_parametros = {
    'dbname': 'geservapp',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432'  
}


class ConexionBD:
    conexion = None 
    db_parametros = None
    cursor = None
    

    def __init__(self,db_parametros):
        self.db_parametros = db_parametros


    def realizar_conexion(self ):
        try:
            self.conexion= psycopg2.connect(**self.db_parametros)
            print(f"conexion para la base {self.db_parametros['dbname']} fue realizada correctamente")
            self.cursor= self.conexion.cursor()
        except psycopg2.Error as e:
            print("Error al conectar a la base de datos:", e)


    def probar_consulta(self,query):
        self.cursor.execute(query)
        registro = self.cursor.fetchall()
        df = pd.DataFrame(registro)
        print(df)



conexion_agendaza = ConexionBD(agendaza_db_parametros)
conexion_agendaza.realizar_conexion()
conexion_agendaza.probar_consulta('select * from usuario')




        


    

     
    

