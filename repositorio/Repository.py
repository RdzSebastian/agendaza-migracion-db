from abc import ABC, abstractmethod
from sqlalchemy.orm import sessionmaker
from typing import TypeVar, Generic

from model.geserveapp.UsuarioLegacy import UsuarioLegacy

T = TypeVar('T')  # Define un tipo genérico T


class Repositorio(ABC, Generic[T]):
    def __init__(self, session: sessionmaker):
        self.session = session()

    def save(self, obj: T):
        self.session.add(obj)
        self.session.commit()

    def getAll(self):
        pass


class UsuarioLegacyRepository(Repositorio[UsuarioLegacy]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)

