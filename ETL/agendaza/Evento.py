from sqlalchemy import Column, Integer, String, BigInteger, Date, UniqueConstraint, func, Boolean, Float
from ETL.Conexión import conexionAgendaza
from datetime import date


class Evento(conexionAgendaza.Base):
    __tablename__ = 'evento'

    id = Column(Integer, primary_key=True, autoincrement=True)
    anotaciones = Column(String)
    catering_otro = Column(Float)
    catering_otro_descripcion = Column(String)
    codigo = Column(String)
    descuento = Column(Integer)
    estado = Column(String)
    extra_otro = Column(Integer)
    fin = Column(Date)
    inicio = Column(Date)
    nombre = Column(String)
    capacidad_id = Column(Integer)
    cliente_id = Column(Integer)
    empresa_id = Column(Integer)
    encargado_id = Column(Integer)
    tipo_evento_id = Column(Integer)
    evento_id_legacy = Column(Integer)

    def __init__(self, catering_otro=None,
                 codigo=None, descuento=None, estado=None, extra_otro=None, fin=None,
                 inicio=None, nombre=None, capacidad_id=None, cliente_id=None,
                 empresa_id=None, encargado_id=None, tipo_evento_id=None , evento_id_legacy = None):
        self.anotaciones = ""
        self.catering_otro = catering_otro
        self.catering_otro_descripcion = ""
        self.codigo = codigo
        self.descuento = descuento
        self.estado = estado
        self.extra_otro = extra_otro
        self.fin = fin
        self.inicio = inicio
        self.nombre = nombre
        self.capacidad_id = capacidad_id
        self.cliente_id = cliente_id
        self.empresa_id = empresa_id
        self.encargado_id = encargado_id
        self.tipo_evento_id = tipo_evento_id
        self.evento_id_legacy = evento_id_legacy
