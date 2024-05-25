from sqlalchemy import Column, ForeignKey, Integer, String, Date, BigInteger
from ETL.Conexión import conexionGeserveApp
from ETL.agendaza.Empresa import Empresa
from ETL.gerservapp_legacy.Legacy import Legacy


class SalonLegacy(conexionGeserveApp.Base, Legacy):
    __tablename__ = 'salon'
    id = Column(Integer, primary_key=True, autoincrement=True)
    calle = Column(Integer)
    municipio = Column(String)
    nombre = Column(String)
    numero = Column(Integer)
    id_agendaza = Column(Integer, unique=True)

    empresa = None

    def conversion(self):
        empresaARetornar = Empresa(
            self.nombre,
            111111111,
            'miixeventos1@gmail.com',
            self.calle,
            self.numero,
            self.municipio,
            self.id,
            'Salon'
        )

        self.empresa = empresaARetornar;

        return empresaARetornar

    def asignarIdAgendaza(self):
        self.id_agendaza = self.empresa.id


