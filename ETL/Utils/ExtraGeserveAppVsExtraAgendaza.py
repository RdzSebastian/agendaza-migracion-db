class ExtraGeserveAppVsExtraAgendaza:
    id_agendaza = None;
    id_legacy = None
    id_empresa = None;
    id_empresa_legacy = None

    def __init__(self, id_agendaza, id_legacy ,id_empresa , id_empresa_legacy):
        self.id_agendaza = id_agendaza
        self.id_legacy = id_legacy
        self.id_empresa = id_empresa
        self.id_empresa_legacy = id_empresa_legacy

