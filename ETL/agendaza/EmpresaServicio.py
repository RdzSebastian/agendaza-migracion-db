from ETL.Conexión import conexionAgendaza


class EmpresaServicio(conexionAgendaza.Base):
    def __init__(self, empresa_id=None, servicio_id=None):
        self.empresa_id = empresa_id
        self.servicio_id = servicio_id
