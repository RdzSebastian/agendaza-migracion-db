from sqlalchemy.orm import sessionmaker
from repositorio.Repository import Repositorio
from ETL.agendaza.Empresa import Empresa


class EmpresaRepository(Repositorio[Empresa]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)
