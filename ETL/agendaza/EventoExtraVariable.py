from sqlalchemy import Column, Integer, String, BigInteger, Date, UniqueConstraint, func, Boolean
from ETL.Conexión import conexionAgendaza
from datetime import date


class EventoExtraVariable(conexionAgendaza.Base):
    __tablename__ = 'evento_extra_variable'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cantidad = Column(Integer, nullable=False)
    evento_id = Column(BigInteger, nullable=False)
    extra_id = Column(BigInteger, nullable=False)
    id_legacy = Column(BigInteger)

    def __init__(self, cantidad, evento_id, extra_id ,id_legacy):
        self.cantidad = cantidad
        self.evento_id = evento_id
        self.extra_id = extra_id
        self.id_legacy = id_legacy

