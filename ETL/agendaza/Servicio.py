from sqlalchemy import Column, Integer, String, BigInteger, Date
from ETL.Conexión import conexionAgendaza


class Servicio(conexionAgendaza.Base):
    __tablename__ = 'servicio'

    id = Column(BigInteger, primary_key=True, nullable=False)
    fecha_baja = Column(Date, nullable=True)
    empresa_id = Column(BigInteger, nullable=True)
    nombre = Column(String(255), nullable=True)

    def __init__(self, fecha_baja=None, empresa_id=None, nombre=None):
        self.fecha_baja = fecha_baja
        self.empresa_id = empresa_id
        self.nombre = nombre
