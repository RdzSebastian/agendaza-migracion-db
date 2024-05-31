from sqlalchemy import Column, ForeignKey, Integer, String, Date, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from ETL.Conexión import conexionGeserveApp
from ETL.agendaza.Extra import Extra
from ETL.gerservapp_legacy.Legacy import Legacy
from ETL.agendaza.Usuario import Usuario


class PrecioConFechaLegacy(conexionGeserveApp.Base, Legacy):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    precio = Column(Integer)
    desde = Column(Date)
    hasta = Column(Date)


class PrecioConFechaTipoCatering(PrecioConFechaLegacy):
    __tablename__ = 'precio_con_fecha_tipo_catering'
    tipo_catering_id = Column(Integer, ForeignKey('tipo_catering.id'))


class PrecioConFechaSubTipoEvento(PrecioConFechaLegacy):
    __tablename__ = 'precio_con_fecha_extra_sub_tipo_evento'
    extra_sub_tipo_evento_id = Column(Integer, ForeignKey('extra_sub_tipo_evento.id'))


class PrecioConFechaExtraVariableCatering(PrecioConFechaLegacy):
    __tablename__ = 'precio_con_fecha_extra_variable_catering'
    extra_variable_catering_id = Column(Integer, ForeignKey('extra_variable_catering.id'))


class PrecioConFechaExtraVariableSubTipoEvento(PrecioConFechaLegacy):
    __tablename__ = 'precio_con_fecha_extra_variable_sub_tipo_evento'
    extra_variable_sub_tipo_evento_id = Column(Integer, ForeignKey('extra_variable_sub_tipo_evento.id'))
