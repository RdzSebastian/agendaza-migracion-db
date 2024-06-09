from sqlalchemy.orm import sessionmaker

from ETL.agendaza.Capacidad import Capacidad
from repositorio.Repository import Repositorio


class CapacidadRepository(Repositorio[Capacidad]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)
