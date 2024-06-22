from sqlalchemy.orm import sessionmaker

from ETL.agendaza.EventoExtra import EventoExtra
from repositorio.Repository import Repositorio
from ETL.agendaza.Empresa import Empresa


class EventoExtraRepository(Repositorio[EventoExtra]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)
