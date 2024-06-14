from sqlalchemy import Column, Integer, String, BigInteger, Date, UniqueConstraint, func, Boolean
from ETL.Conexión import conexionAgendaza
from datetime import date


class PrecioConFechaEvento(conexionAgendaza.Base):
    __tablename__ = 'precio_con_fecha_evento'
    id = Column(Integer, primary_key=True, autoincrement=True)
    desde = Column(Date)
    hasta = Column(Date)
    precio = Column(Integer)
    empresa_id = Column(Integer)
    tipo_evento_id = Column(Integer)

    def __init__(self, desde, hasta, precio, empresa_id, tipo_evento_id):
        self.desde = desde
        self.hasta = hasta
        self.precio = precio
        self.empresa_id = empresa_id
        self.tipo_evento_id = tipo_evento_id



