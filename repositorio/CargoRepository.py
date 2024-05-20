from sqlalchemy.orm import sessionmaker
from repositorio.Repository import Repositorio
from ETL.agendaza.Cargo import Cargo


class CargoRepository(Repositorio[Cargo]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)
