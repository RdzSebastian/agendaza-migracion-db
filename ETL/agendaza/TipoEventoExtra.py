from sqlalchemy import Column, Integer, String, BigInteger, Date
from ETL.Conexión import conexionAgendaza


class TipoEventoExtra(conexionAgendaza.Base):
    __tablename__ = 'tipo_evento_extra'

    tipo_evento_id = Column(BigInteger, primary_key=True, nullable=False)
    extra_id = Column(BigInteger, primary_key=True, nullable=False)

    tipo_evento_id_legacy = Column(Integer, nullable=False)

    extra_tipo_catering_id_legacy = Column(Integer, nullable=False)
    extra_sub_tipo_evento_id_legacy = Column(Integer, nullable=False)
    extra_sub_tipo_evento_variable_catering = Column(Integer, nullable=False)
    extra_sub_tipo_evento_extra_variable_catering = Column(Integer, nullable=False)

    def __init__(self, tipo_evento_id, tipo_evento_id_legacy, extra_id):
        self.tipo_evento_id = tipo_evento_id
        self.tipo_evento_id_legacy = tipo_evento_id_legacy
        self.extra_id = extra_id

    def asignarIdLegacy(self, tipo, id):
        if tipo == "TIPO_CATERING":
            self.extra_tipo_catering_id_legacy = id

        if tipo == "EVENTO":
            self.extra_sub_tipo_evento_id_legacy = id

        if tipo == "VARIABLE_EVENTO":
            self.extra_sub_tipo_evento_variable_catering = id

        if tipo == "VARIABLE_CATERING":
            self.extra_sub_tipo_evento_extra_variable_catering = id
