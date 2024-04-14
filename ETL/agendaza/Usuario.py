from sqlalchemy import Column, Integer, String, BigInteger, Date
from sqlalchemy.ext.declarative import declarative_base
from ETL.Conexión import conexionAgendaza
from datetime import date
from sqlalchemy import func

Base = declarative_base()


class Usuario(conexionAgendaza.Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    celular = Column(BigInteger)
    email = Column(String)
    username = Column(String, default='')
    password = Column(String, default='')
    fecha_nacimiento = Column(Date, default=func.current_date())
    fecha_alta = Column(Date)
    fecha_baja = Column(Date, nullable=True)
    id_legacy = Column(Integer, unique=True)


    def __init__(self, nombre, apellido, email, username='', password=''):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.username = username
        self.password = password
        self.fecha_alta = date.today()
        self.fechaNacimiento = date.today()
        self.celular = 0

    def establecerFechaBajaSiCorresponde(self, enabled: bool):
        if not enabled:
            self.fecha_baja = date.today()
