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

    def listaPrecioFechas(self):

        lista = self.obtenerPrecioFechas()
        listaARetornar = []

        for item in lista:
            if item.precio != 0:
                listaARetornar.append(item)

        return listaARetornar

    def obtenerPrecioFechas(self):
        pass


class ExtraVariableCatering(ExtraLegacy):
    __tablename__ = 'extra_variable_catering'

    def tipoeExtra(self):
        return 'VARIABLE_CATERING'

    def asignarIdLegacy(self):
        self.extraARetornar.extra_variable_catering_id_legacy = self.id

    def obtenerPrecioFechas(self):
        return self.precio_fechas


class ExtraSubTipoEvento(ExtraLegacy):
    __tablename__ = 'extra_sub_tipo_evento'

    def tipoeExtra(self):
        return 'EVENTO'

    def asignarIdLegacy(self):
        self.extraARetornar.extra_sub_tipo_evento_id_legacy = self.id

    def obtenerPrecioFechas(self):
        return self.precio_fechas


class ExtraTipoCatering(ExtraLegacy):
    __tablename__ = 'tipo_catering'

    def tipoeExtra(self):
        return 'TIPO_CATERING'

    def asignarIdLegacy(self):
        self.extraARetornar.tipo_catering_id_legacy = self.id

    def obtenerPrecioFechas(self):
        return self.precio_fechas


class ExtraVariableSubTipoEvento(ExtraLegacy):
    __tablename__ = 'extra_variable_sub_tipo_evento'

    def tipoeExtra(self):
        return 'VARIABLE_EVENTO'

    def asignarIdLegacy(self):
        self.extraARetornar.extra_variable_sub_tipo_evento_id_legacy = self.id

    def obtenerPrecioFechas(self):
        return self.precio_fechas
