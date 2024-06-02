from sqlalchemy.orm import sessionmaker

from ETL.agendaza.PrecioConFechaExtra import PrecioConFechaExtra
from repositorio.Repository import Repositorio
from ETL.agendaza.Empresa import Empresa


class PrecioConFechaExtraRepository(Repositorio[PrecioConFechaExtra]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)
