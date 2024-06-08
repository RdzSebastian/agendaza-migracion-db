from sqlalchemy.orm import sessionmaker

from ETL.agendaza.Extra import Extra
from ETL.gerservapp_legacy.PrecioConFechaLegacy import PrecioConFechaTipoCatering
from repositorio.Repository import Repositorio


class ExtraRepository(Repositorio[Extra]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)



