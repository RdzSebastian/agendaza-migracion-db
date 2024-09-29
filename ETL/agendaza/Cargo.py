from sqlalchemy import Column, Integer, String, BigInteger, Date, UniqueConstraint, func, Boolean
from ETL.Conexión import conexionAgendaza
from datetime import date


class Cargo(conexionAgendaza.Base):
    __tablename__ = 'cargo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer)
    tipo_cargo = Column(String)
    empresa_id = Column(Integer)
    es_legacy = Column(Boolean)

    def __init__(self, usuario_id, tipo_cargo):
        self.usuario_id = usuario_id
        self.tipo_cargo = tipo_cargo

    def setEmpresaId(self, empresaList, salon_id_legacy):
        for empresa in empresaList:
            if empresa.id_legacy == salon_id_legacy:
                self.empresa_id = empresa.id

    def correccionTipoCargo(self):
        if self.tipo_cargo == "USER":
            self.tipo_cargo = "ENCARGADO"

