from sqlalchemy import Column, Integer, String, BigInteger, Date
from ETL.Conexión import conexionAgendaza


class TipoEventoExtra(conexionAgendaza.Base):
    __tablename__ = 'tipo_evento_extra'

    tipo_evento_id = Column(BigInteger, primary_key=True, nullable=False)
    extra_id = Column(BigInteger, primary_key=True, nullable=False)

    tipo_evento_id_legacy = Column(BigInteger)
    extra_id_legacy = Column(BigInteger)

    def __init__(self, tipo_evento_id, servicio_id, tipo_evento_id_legacy, extra_id_legacy):
        self.tipo_evento_id = tipo_evento_id
        self.servicio_id = servicio_id
        self.tipo_evento_id_legacy = tipo_evento_id_legacy
        self.extra_id_legacy = extra_id_legacy
