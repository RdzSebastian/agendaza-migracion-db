from sqlalchemy import Column, Integer, String, BigInteger, Date, UniqueConstraint, func, Boolean, DateTime
from ETL.Conexión import conexionAgendaza
from datetime import date


class Pago(conexionAgendaza.Base):
    __tablename__ = 'pago'

    id = Column(BigInteger, primary_key=True, nullable=False)
    fecha = Column(DateTime, nullable=True)
    medio_de_pago = Column(String(255), nullable=True)
    monto = Column(Integer, nullable=True)
    encargado_id = Column(BigInteger, nullable=True)
    evento_id = Column(BigInteger, nullable=True)

    def __init__(self, id, fecha=None, medio_de_pago=None, monto=None, encargado_id=None, evento_id=None):
        self.id = id
        self.fecha = fecha
        self.medio_de_pago = medio_de_pago
        self.monto = monto
        self.encargado_id = encargado_id
        self.evento_id = evento_id

