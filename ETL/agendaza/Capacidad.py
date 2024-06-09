from sqlalchemy import Column, Integer, String, BigInteger, Date, UniqueConstraint, func, Boolean
from ETL.Conexión import conexionAgendaza


class Capacidad(conexionAgendaza.Base):
    __tablename__ = 'capacidad'

    id = Column(Integer, primary_key=True, autoincrement=True)
    capacidad_adultos = Column(Integer)
    capacidad_ninos = Column(String)

    def __init__(self, capacidad_adultos, capacidad_ninos):
        self.capacidad_adultos = capacidad_adultos
        self.capacidad_ninos = capacidad_ninos
