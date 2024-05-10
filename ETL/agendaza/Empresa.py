from sqlalchemy import Column, Integer, String, BigInteger, Date, UniqueConstraint, func
from ETL.Conexión import conexionAgendaza
from datetime import date


class Empresa(conexionAgendaza.Base):
    __tablename__ = 'empresa'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    telefono = Column(Integer)
    email = Column(String)
    calle = Column(String)
    numero = Column(Integer)
    municipio = Column(String)
    id_legacy = Column(Integer, unique=True)
    dtype = Column(String)

    def __init__(self, nombre, telefono, email, calle, numero, municipio, id_legacy , dtype):
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.calle = calle
        self.numero = numero
        self.municipio = municipio
        self.id_legacy = id_legacy
        self.dtype = dtype
