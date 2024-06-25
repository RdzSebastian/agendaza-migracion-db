from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker

from ETL.agendaza.PrecioConFechaExtra import PrecioConFechaExtra
from ETL.gerservapp_legacy.PrecioConFechaLegacy import PrecioConFechaTipoCatering, PrecioConFechaSubTipoEvento, \
    PrecioConFechaExtraVariableCatering, PrecioConFechaExtraVariableSubTipoEvento
from repositorio.Repository import Repositorio, T
from ETL.agendaza.Empresa import Empresa


class PrecioConFechaExtraRepository(Repositorio[PrecioConFechaExtra]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)


class PrecioConFechaExtraVariableCateringRepository(Repositorio[PrecioConFechaExtraVariableCatering]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)

    async def getAll(self) -> list[PrecioConFechaExtraVariableCatering]:
        try:
            return self.session.query(PrecioConFechaExtraVariableCatering).filter(
                PrecioConFechaExtraVariableCatering.precio != 0).all()
        except NoResultFound:
            return []


class PrecioConFechaExtraSubTipoEventoRepository(Repositorio[PrecioConFechaSubTipoEvento]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)

    async def getAll(self) -> list[PrecioConFechaSubTipoEvento]:
        try:
            return self.session.query(PrecioConFechaSubTipoEvento).filter(
                PrecioConFechaSubTipoEvento.precio != 0).all()
        except NoResultFound:
            return []


class PrecioConFechaExtraTipoCateringRepository(Repositorio[PrecioConFechaTipoCatering]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)

    async def getAll(self) -> list[PrecioConFechaTipoCatering]:
        try:
            return self.session.query(PrecioConFechaTipoCatering).filter(
                PrecioConFechaTipoCatering.precio != 0).all()
        except NoResultFound:
            return []


class PrecioConFechaExtraVariableEventoRepository(Repositorio[PrecioConFechaExtraVariableSubTipoEvento]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)

    async def getAll(self) -> list[PrecioConFechaExtraVariableSubTipoEvento]:
        try:
            return self.session.query(PrecioConFechaExtraVariableSubTipoEvento).filter(
                PrecioConFechaExtraVariableSubTipoEvento.precio != 0).all()
        except NoResultFound:
            return []
