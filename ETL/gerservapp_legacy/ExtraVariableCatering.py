from sqlalchemy import Column, ForeignKey, Integer, String, Date, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from ETL.Conexión import conexionGeserveApp
from ETL.agendaza.Extra import Extra
from ETL.gerservapp_legacy.Legacy import Legacy
from ETL.agendaza.Usuario import Usuario


class ExtraVariableCatering(conexionGeserveApp.Base, Legacy):
    __tablename__ = 'extra_variable_catering'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)

    def conversion(self):
        extraARetornar = Extra(nombre=self.nombre,
                               tipo_extra='VARIABLE_CATERING'
                               )

        extraARetornar.extra_variable_catering_id_legacy = self.id
        return extraARetornar

    def __repr__(self):
        return (f"<Extra(id={self.id}, nombre='{self.nombre}', tipo_extra='{self.tipo_extra}', "
                f"empresa_id={self.empresa_id}, extra_variable_catering_id_legacy={self.extra_variable_catering_id_legacy}, "
                f"fecha_baja={self.fecha_baja})>")

