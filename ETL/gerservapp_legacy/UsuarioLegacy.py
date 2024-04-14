from abc import ABC

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean

from sqlalchemy.orm import relationship
from ETL.Conexión import conexionGeserveApp
from ETL.gerservapp_legacy.Legacy import Legacy
from ETL.agendaza.Usuario import Usuario
from datetime import datetime


##Si una clase hereda de el entonces esa clase puede ser mapeable a una BD


class UsuarioLegacy(conexionGeserveApp.Base, Legacy):
    __tablename__ = 'usuario'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    nombre = Column(String)
    apellido = Column(String)
    mail = Column(String)
    username = Column(String)
    password = Column(String)

    account_non_expired = Column(Boolean)
    account_non_locked = Column(Boolean)
    credentials_non_expired = Column(Boolean)
    enabled = Column(Boolean)
    id_agendaza = Column(Integer, unique=True, default=0)

    usuarioAgendaza = None

    def __init__(self, nombre, apellido, mail, username, password,
                 account_non_expired=True, account_non_locked=True,
                 credentials_non_expired=True, enabled=True):
        self.nombre = nombre
        self.apellido = apellido
        self.mail = mail
        self.username = username
        self.password = password
        self.account_non_expired = account_non_expired
        self.account_non_locked = account_non_locked
        self.credentials_non_expired = credentials_non_expired
        self.enabled = enabled

    def conversion(self):
        usuarioARetornar = Usuario(nombre=self.nombre,
                                   apellido=self.apellido,
                                   email=self.mail,
                                   username=self.username,
                                   password=self.password,
                                   id_legacy=self.id)
        usuarioARetornar.establecerFechaBajaSiCorresponde(self.enabled)

        self.usuarioAgendaza = usuarioARetornar

        return usuarioARetornar

    def asignarIdAgendaza(self):
        self.id_agendaza = self.usuarioAgendaza.id
