from sqlalchemy.orm import sessionmaker
from repositorio.Repository import Repositorio
from ETL.gerservapp_legacy.ClienteLegacy import ClienteLegacy


class ClienteLegacyRepository(Repositorio[ClienteLegacy]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)
