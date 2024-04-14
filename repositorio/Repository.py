from abc import ABC, abstractmethod
from sqlalchemy.orm import sessionmaker
from typing import TypeVar, Generic
from typing import Type
from ETL.gerservapp_legacy.UsuarioLegacy import UsuarioLegacy
from typing import List

T = TypeVar('T')  # Define un tipo genérico T


class Repositorio(ABC, Generic[T]):

    def __init__(self, session: sessionmaker):
        self.session = session()

    def save(self, obj: T):
        self.session.add(obj)
        self.session.commit()

    @classmethod
    def obtenerClase(cls) -> Type[T]:
        return cls.__orig_bases__[0].__args__[0]

    def getAll(self) -> list[T]:
        clase = self.obtenerClase()
        return self.session.query(clase).all()

    def saveAll(self, objs: List[T]):
        for obj in objs:
            self.session.add(obj)
        self.session.commit()


class UsuarioLegacyRepository(Repositorio[UsuarioLegacy]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)
