from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker

from ETL.agendaza.PrecioConFechaExtra import PrecioConFechaExtra
from ETL.agendaza.TipoEvento import TipoEvento
from ETL.gerservapp_legacy.PrecioConFechaLegacy import PrecioConFechaTipoCatering, PrecioConFechaSubTipoEvento, \
    PrecioConFechaExtraVariableCatering, PrecioConFechaExtraVariableSubTipoEvento
from repositorio.Repository import Repositorio, T
from ETL.agendaza.Empresa import Empresa


class TipoEventoRepository(Repositorio[TipoEvento]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)