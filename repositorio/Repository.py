from abc import ABC, abstractmethod
from sqlalchemy.orm import sessionmaker
from typing import TypeVar, Generic
from typing import Type
from ETL.gerservapp_legacy.UsuarioLegacy import UsuarioLegacy
from typing import List
from sqlalchemy import text

T = TypeVar('T')  # Define un tipo genérico T

import asyncio


class Repositorio(ABC, Generic[T]):

    def __init__(self, session: sessionmaker):
        self.session = session()

    async def save(self, obj: T):
        self.session.add(obj)
        self.session.commit()

    @classmethod
    async def obtenerClase(cls) -> Type[T]:
        return cls.__orig_bases__[0].__args__[0]

    async def getAll(self) -> List[T]:
        clase = await self.obtenerClase()
        return self.session.query(clase).order_by(clase.id).all()

    async def saveAll(self, objs: List[T]):
        for obj in objs:
            self.session.add(obj)
        self.session.commit()

    async def sqlNativeQuery(self, query: str):
        retornar = self.session.execute(text(query))
        self.session.commit()
        return retornar

    async def rollback(self):
        self.session.rollback()


class UsuarioLegacyRepository(Repositorio[UsuarioLegacy]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)
