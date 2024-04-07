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


try:
    conexion_agendaza= psycopg2.connect(**agendaza_db_parametros)
    print("conexion para la bd de agendaza realizada con exito")
except psycopg2.Error as e:
    print("Error al conectar a la base de datos:", e)



try:
    conexion_gersevapp= psycopg2.connect(**geservapp_db_parametros)
    print("conexion para la bd de geservapp realizada con exito")
except psycopg2.Error as e:
    print("Error al conectar a la base de datos:", e)


cursor_agendaza =  conexion_agendaza.cursor()
query = 'SELECT * FROM  usuario'
cursor_agendaza.execute(query)
registros = cursor_agendaza.fetchall()




df = pd.DataFrame(registros)
print(df)



