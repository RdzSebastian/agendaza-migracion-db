from sqlalchemy.orm import sessionmaker

from repositorio.EmpresaRepository import EmpresaRepository
from repositorio.Repository import Repositorio


class EmpresaServicioRepository(Repositorio[EmpresaRepository]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)
