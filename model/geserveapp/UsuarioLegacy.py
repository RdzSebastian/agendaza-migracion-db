from abc import ABC, abstractmethod
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, exc
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()  ##Si una clase hereda de el entonces esa clase puede ser mapeable a una BD


class UsuarioLegacy(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    mail = Column(String)
    username = Column(String)
    password = Column(String)

    account_non_expired = Column(Boolean)
    account_non_locked = Column(Boolean)
    credentials_non_expired = Column(Boolean)
    enabled = Column(Boolean)
