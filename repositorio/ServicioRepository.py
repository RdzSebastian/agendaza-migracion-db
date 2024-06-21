from sqlalchemy.orm import sessionmaker

from ETL.agendaza.Servicio import Servicio
from repositorio.Repository import Repositorio


class ServicioRepository(Repositorio[Servicio]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)
