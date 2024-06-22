from sqlalchemy.orm import sessionmaker

from ETL.agendaza.Evento import Evento
from ETL.agendaza.EventoExtraVariable import EventoExtraVariable
from repositorio.Repository import Repositorio
from ETL.agendaza.Empresa import Empresa


class EventoExtraVariableRepository(Repositorio[EventoExtraVariable]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)
