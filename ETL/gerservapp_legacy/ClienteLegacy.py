from sqlalchemy import Column, ForeignKey, Integer, String, Date, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from ETL.Conexión import conexionGeserveApp
from ETL.gerservapp_legacy.Legacy import Legacy
from ETL.agendaza.Usuario import Usuario


class ClienteLegacy(conexionGeserveApp.Base, Legacy):
    __tablename__ = 'cliente'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String)
    celular = Column(BigInteger)



    def conversion(self):
        usuarioARetornar = Usuario(nombre=self.nombre,
                                   apellido=self.apellido,
                                   email=self.email,
                                   celular=self.celular,
                                   id_cliente_legacy=self.id)

        return usuarioARetornar
