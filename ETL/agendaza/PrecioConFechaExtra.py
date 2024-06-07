from sqlalchemy import Column, Integer, String, BigInteger, Date, UniqueConstraint, func, Boolean
from ETL.Conexión import conexionAgendaza
from datetime import date


class PrecioConFechaExtra(conexionAgendaza.Base):
    __tablename__ = 'precio_con_fecha_extra'
    id = Column(Integer, primary_key=True, autoincrement=True)
    desde = Column(Date)
    fecha_baja = Column(Date)
    hasta = Column(Date)
    precio = Column(Integer)
    empresa_id = Column(Integer)
    extra_id = Column(Integer)

    def __init__(self, desde, fecha_baja, hasta, precio,empresa_id,extra_id):
        self.desde = desde
        self.fecha_baja = fecha_baja
        self.hasta = hasta
        self.precio = precio
        self.empresa_id = empresa_id
        self.extra_id = extra_id
