from sqlalchemy.orm import sessionmaker

from ETL.agendaza.PrecioConFechaEvento import PrecioConFechaEvento

from repositorio.Repository import Repositorio, T


class PrecioConFechaEventoRepository(Repositorio[PrecioConFechaEvento]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)


