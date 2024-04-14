from sqlalchemy import Column, Integer, String, BigInteger, Date, UniqueConstraint, func
from ETL.Conexión import conexionAgendaza
from datetime import date


class Usuario(conexionAgendaza.Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    celular = Column(BigInteger)
    email = Column(String)
    username = Column(String, default='')
    password = Column(String, default='')
    fecha_nacimiento = Column(Date, default=func.current_date())
    fecha_alta = Column(Date, default=date.today())
    fecha_baja = Column(Date, nullable=True)
    id_usuario_legacy = Column(Integer, unique=True)

    def __init__(self, nombre, apellido, email, username, password, id_usuario_legacy):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.username = username
        self.password = password
        self.fecha_alta = date.today()
        self.fecha_nacimiento = date.today()
        self.celular = 0
        self.id_usuario_legacy = id_usuario_legacy

    def establecerFechaBajaSiCorresponde(self, enabled: bool):
        if not enabled:
            self.fecha_baja = date.today()
