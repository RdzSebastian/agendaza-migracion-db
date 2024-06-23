from sqlalchemy import Column, Integer, String, BigInteger, Date, UniqueConstraint, func, Boolean, DateTime
from ETL.Conexión import conexionAgendaza
from datetime import date


class PrecioConFechaExtra(conexionAgendaza.Base):
    __tablename__ = 'precio_con_fecha_extra'
    id = Column(Integer, primary_key=True, autoincrement=True)
    desde = Column(DateTime)
    fecha_baja = Column(Date)
    hasta = Column(DateTime)
    precio = Column(Integer)
    empresa_id = Column(Integer)
    extra_id = Column(Integer)
    extra_variable_catering_legacy = Column(Integer)
    extra_variable_sub_tipo_evento_legacy = Column(Integer)
    extra_sub_tipo_evento_legacy = Column(Integer)
    extra_tipo_catering_legacy = Column(Integer)

    def __init__(self, desde, fecha_baja, hasta, precio,empresa_id,extra_id):
        self.desde = desde
        self.fecha_baja = fecha_baja
        self.hasta = hasta
        self.precio = precio
        self.empresa_id = empresa_id
        self.extra_id = extra_id
