from sqlalchemy import Column, Integer, String, BigInteger, Date
from ETL.Conexión import conexionAgendaza


class EventoExtra(conexionAgendaza.Base):
    __tablename__ = 'evento_extra'

    evento_id = Column(BigInteger, primary_key=True, nullable=False)
    extra_id = Column(BigInteger, primary_key=True, nullable=False)
    evento_id_legacy = Column(BigInteger, primary_key=True, nullable=False)
    extra_id_legacy = Column(BigInteger, primary_key=True, nullable=False)

    def __init__(self, evento_id, extra_id, evento_id_legacy, extra_id_legacy):
        self.evento_id = evento_id
        self.extra_id = extra_id
        self.evento_id_legacy = evento_id_legacy
        self.extra_id_legacy = extra_id_legacy
