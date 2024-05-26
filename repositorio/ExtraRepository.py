from sqlalchemy.orm import sessionmaker

from ETL.agendaza.Extra import Extra
from ETL.gerservapp_legacy.ExtraLegacy import ExtraVariableCatering, ExtraLegacy, ExtraSubTipoEvento, ExtraTipoCatering, \
    ExtraVariableSubTipoEvento
from repositorio.Repository import Repositorio


class ExtraRepository(Repositorio[Extra]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)


class ExtraVariableCateringLegacyRepository(Repositorio[ExtraVariableCatering]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)


class ExtraSubTipoEventoLegacyRepository(Repositorio[ExtraSubTipoEvento]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)


class ExtraSubTipoCateringLegacyRepository(Repositorio[ExtraTipoCatering]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)


class ExtraVariableSubTipoEventoRepository(Repositorio[ExtraVariableSubTipoEvento]):
    def __init__(self, session: sessionmaker):
        super().__init__(session)