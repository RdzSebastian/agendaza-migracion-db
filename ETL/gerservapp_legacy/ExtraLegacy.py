from sqlalchemy import Column, ForeignKey, Integer, String, Date, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from ETL.Conexión import conexionGeserveApp
from ETL.agendaza.Extra import Extra
from ETL.gerservapp_legacy.Legacy import Legacy
from ETL.agendaza.Usuario import Usuario


class ExtraLegacy(conexionGeserveApp.Base, Legacy):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    extraARetornar = None

    def tipoeExtra(self):
        pass

    def asignarIdLegacy(self):
        pass

    def conversion(self):
        self.extraARetornar = Extra(nombre=self.nombre,
                                    tipo_extra=self.tipoeExtra()
                                    )
        self.asignarIdLegacy()
        return self.extraARetornar


class ExtraVariableCatering(ExtraLegacy):
    __tablename__ = 'extra_variable_catering'

    def tipoeExtra(self):
        return 'VARIABLE_CATERING'

    def asignarIdLegacy(self):
        self.extraARetornar.extra_variable_catering_id_legacy = self.id
