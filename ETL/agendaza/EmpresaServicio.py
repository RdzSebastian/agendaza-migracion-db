from sqlalchemy import Column, Integer
from ETL.Conexión import conexionAgendaza


class EmpresaServicio(conexionAgendaza.Base):
    __tablename__ = 'empresa_servicio'

    empresa_id = Column(Integer, primary_key=True)
    servicio_id = Column(Integer, primary_key=True)
    empresa_id_legacy = Column(Integer)
    servicio_id_legacy = Column(Integer)

    def __init__(self, empresa_id=None, servicio_id=None, empresa_id_legacy=None, servicio_id_legacy=None):
        self.empresa_id = empresa_id
        self.servicio_id = servicio_id
        self.empresa_id_legacy = empresa_id_legacy
        self.servicio_id_legacy = servicio_id_legacy
