from abc import ABC, abstractmethod
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, exc
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean

from sqlalchemy.orm import relationship
from ETL.Conexión import conexionGeserveApp


##Si una clase hereda de el entonces esa clase puede ser mapeable a una BD


class UsuarioLegacy(conexionGeserveApp.Base):
    __tablename__ = 'usuario'

    id = Column(Integer(), primary_key=True,autoincrement=True)
    nombre = Column(String)
    apellido = Column(String)
    mail = Column(String)
    username = Column(String)
    password = Column(String)

    account_non_expired = Column(Boolean)
    account_non_locked = Column(Boolean)
    credentials_non_expired = Column(Boolean)
    enabled = Column(Boolean)

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
