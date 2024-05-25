from sqlalchemy.orm import sessionmaker

from repositorio.Repository import Repositorio
from ETL.gerservapp_legacy.SalonLegacy import SalonLegacy


class SalonLegacyRepositorio(Repositorio[SalonLegacy]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)
