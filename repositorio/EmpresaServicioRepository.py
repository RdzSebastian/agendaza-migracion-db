from sqlalchemy.orm import sessionmaker

from ETL.agendaza.EmpresaServicio import EmpresaServicio
from repositorio.EmpresaRepository import EmpresaRepository
from repositorio.Repository import Repositorio


class EmpresaServicioRepository(Repositorio[EmpresaServicio]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)
