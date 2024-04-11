from sqlalchemy import Column, Integer, String, BigInteger, Date
from sqlalchemy.ext.declarative import declarative_base
from ETL.Conexión import conexionAgendaza

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    celular = Column(BigInteger)
    email = Column(String)
    username = Column(String, default='')
    password = Column(String, default='')
    fechaNacimiento = Column(Date)
    fechaAlta = Column(Date)
    fechaBaja = Column(Date, nullable=True)

    def __init__(self, nombre, apellido, celular, email, username='', password='', fechaNacimiento=None, fechaAlta=None, fechaBaja=None):
        self.nombre = nombre
        self.apellido = apellido
        self.celular = celular
        self.email = email
        self.username = username
        self.password = password
        self.fechaNacimiento = fechaNacimiento
        self.fechaAlta = fechaAlta
        self.fechaBaja = fechaBaja
