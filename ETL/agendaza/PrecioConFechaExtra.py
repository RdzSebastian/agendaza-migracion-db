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


