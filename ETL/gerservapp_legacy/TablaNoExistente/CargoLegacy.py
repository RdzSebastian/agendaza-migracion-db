from sqlalchemy import Column, ForeignKey, Integer, String, Date, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from ETL.Conexión import conexionGeserveApp
from ETL.gerservapp_legacy.Legacy import Legacy
from ETL.agendaza.Usuario import Usuario


class CargoLegacy(conexionGeserveApp.Base, Legacy):
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer)
    tipo_cargo = Column(String)
    usuario_id = Column(Integer)

    def __init__(self, usuario_id, id, tipo_cargo, empresa_id):
        self.usuario_id = usuario_id
        self.id = id
        self.tipo_cargo = tipo_cargo
        self.empresa_id = empresa_id


