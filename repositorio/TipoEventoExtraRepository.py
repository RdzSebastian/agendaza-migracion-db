from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker

from ETL.agendaza.TipoEventoExtra import TipoEventoExtra
from ETL.agendaza.TipoEventoServicio import TipoEventoServicio

from repositorio.Repository import Repositorio, T


class TipoEventoExtraRepository(Repositorio[TipoEventoExtra]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)
