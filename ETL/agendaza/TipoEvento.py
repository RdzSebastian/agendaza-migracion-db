from sqlalchemy import Column, Integer, String, BigInteger, Date, UniqueConstraint, func, Boolean, Time
from ETL.Conexión import conexionAgendaza
from datetime import date


class TipoEvento(conexionAgendaza.Base):
    __tablename__ = 'tipo_evento'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    duracion = Column(String)
    capacidad_id = Column(Integer)
    cantidad_duracion = Column(Time)
    empresa_id = Column(Integer)
    fecha_baja = Column(Date)
    tipo_evento_legacy = Column(Integer)

    def __init__(self, nombre, duracion, capacidad_id, cantidad_duracion, empresa_id):
        self.nombre = nombre
        self.duracion = duracion
        self.capacidad_id = capacidad_id
        self.cantidad_duracion = cantidad_duracion
        self.empresa_id = empresa_id
