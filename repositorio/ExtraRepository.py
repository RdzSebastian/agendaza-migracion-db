from sqlalchemy.orm import sessionmaker

from ETL.agendaza.Extra import Extra
from ETL.gerservapp_legacy.ExtraLegacy import ExtraVariableCatering, ExtraLegacy, ExtraSubTipoEvento, ExtraTipoCatering, \
    ExtraVariableSubTipoEvento
from ETL.gerservapp_legacy.PrecioConFechaLegacy import PrecioConFechaTipoCatering
from repositorio.Repository import Repositorio


class ExtraRepository(Repositorio[Extra]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)


class ExtraVariableCateringLegacyRepository(Repositorio[ExtraVariableCatering]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)

    def getAll(self):
        return self.session.query(ExtraVariableCatering).join(ExtraVariableCatering.precio_fechas)


class ExtraSubTipoEventoLegacyRepository(Repositorio[ExtraSubTipoEvento]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)

    def getAll(self):
        return self.session.query(ExtraSubTipoEvento).join(ExtraSubTipoEvento.precio_fechas)


class ExtraSubTipoCateringLegacyRepository(Repositorio[ExtraTipoCatering]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)

    def getAll(self):
        return self.session.query(ExtraTipoCatering).join(ExtraTipoCatering.precio_fechas)


class ExtraVariableSubTipoEventoRepository(Repositorio[ExtraVariableSubTipoEvento]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)

    def getAll(self):
        return self.session.query(ExtraVariableSubTipoEvento).join(ExtraVariableSubTipoEvento.precio_fechas)


