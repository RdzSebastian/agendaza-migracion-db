from sqlalchemy import Column, Integer, String, BigInteger, Date, UniqueConstraint, func, Boolean
from ETL.Conexión import conexionAgendaza
from datetime import date


class Extra(conexionAgendaza.Base):
    __tablename__ = 'extra'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_baja = Column(Date)
    nombre = Column(String)
    tipo_extra = Column(String)
    empresa_id = Column(Integer)
    extra_variable_catering_id_legacy = Column(Integer)
    extra_sub_tipo_evento_id_legacy = Column(Integer)
    tipo_catering_id_legacy = Column(Integer)
    extra_variable_sub_tipo_evento_id_legacy = Column(Integer)

    def __init__(self, nombre=None, tipo_extra=None):
        self.nombre = nombre
        self.tipo_extra = tipo_extra
