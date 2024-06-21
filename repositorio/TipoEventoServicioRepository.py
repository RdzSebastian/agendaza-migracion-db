from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker

from ETL.agendaza.TipoEventoServicio import TipoEventoServicio

from repositorio.Repository import Repositorio, T


class TipoEventoServicioRepository(Repositorio[TipoEventoServicio]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)
