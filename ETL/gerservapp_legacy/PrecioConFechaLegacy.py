from sqlalchemy import Column, ForeignKey, Integer, String, Date, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from ETL.Conexión import conexionGeserveApp
from ETL.agendaza.Extra import Extra
from ETL.agendaza.PrecioConFechaExtra import PrecioConFechaExtra
from ETL.gerservapp_legacy.Legacy import Legacy
from ETL.agendaza.Usuario import Usuario


class PrecioConFechaLegacy(conexionGeserveApp.Base, Legacy):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    precio = Column(Integer)
    desde = Column(Date)
    hasta = Column(Date)
    salon_id = Column(Integer)

    empresa_id = None
    extra_id = None

    def __init__(self, precio, desde, hasta, salon_id):
        self.precio = precio
        self.desde = desde
        self.hasta = hasta
        self.salon_id = salon_id

    def conversion(self):
        precioConFechaExtra = PrecioConFechaExtra(
            desde=self.desde,
            fecha_baja=None,
            hasta=self.hasta,
            precio=self.precio,
            empresa_id=self.empresa_id,
            extra_id=self.extra_id
        )
        self.setearIdLegacy(precioConFechaExtra)

        return precioConFechaExtra

    def setearIdLegacy(self, precioConFechaExtra):
        pass


class PrecioConFechaTipoCatering(PrecioConFechaLegacy):
    __tablename__ = 'precio_con_fecha_tipo_catering'
    tipo_catering_id = Column(Integer)

    def idLegacy(self):
        return self.tipo_catering_id

    def setearIdLegacy(self, precioConFechaExtra):
        precioConFechaExtra.extra_tipo_catering_legacy = self.tipo_catering_id


class PrecioConFechaSubTipoEvento(PrecioConFechaLegacy):
    __tablename__ = 'precio_con_fecha_extra_sub_tipo_evento'
    extra_sub_tipo_evento_id = Column(Integer)

    def idLegacy(self):
        return self.extra_sub_tipo_evento_id

    def setearIdLegacy(self, precioConFechaExtra):
        precioConFechaExtra.extra_sub_tipo_evento_legacy = self.extra_sub_tipo_evento_id


class PrecioConFechaExtraVariableCatering(PrecioConFechaLegacy):
    __tablename__ = 'precio_con_fecha_extra_variable_catering'
    extra_variable_catering_id = Column(Integer)

    def idLegacy(self):
        return self.extra_variable_catering_id

    def setearIdLegacy(self, precioConFechaExtra):
        precioConFechaExtra.extra_variable_catering_legacy = self.extra_variable_catering_id


class PrecioConFechaExtraVariableSubTipoEvento(PrecioConFechaLegacy):
    __tablename__ = 'precio_con_fecha_extra_variable_sub_tipo_evento'
    extra_variable_sub_tipo_evento_id = Column(Integer)

    def idLegacy(self):
        return self.extra_variable_sub_tipo_evento_id

    def setearIdLegacy(self, precioConFechaExtra):
        precioConFechaExtra.extra_variable_sub_tipo_evento_legacy = self.extra_variable_sub_tipo_evento_id
