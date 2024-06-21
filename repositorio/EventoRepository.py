from sqlalchemy.orm import sessionmaker

from ETL.agendaza.Evento import Evento
from repositorio.Repository import Repositorio
from ETL.agendaza.Empresa import Empresa


class EventoRepository(Repositorio[Evento]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)
