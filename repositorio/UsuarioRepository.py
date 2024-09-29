from sqlalchemy.orm import sessionmaker
from repositorio.Repository import Repositorio
from ETL.agendaza.Usuario import Usuario


class UsuarioRepository(Repositorio[Usuario]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)