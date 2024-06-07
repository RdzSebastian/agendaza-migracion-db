class ForeignLegacyVsNewAux:
    empresa_id_legacy_vs_agendaza_id = {}

    variableCateringVsAExtraAgendazaList = []
    subTipoEventoVsAExtraAgendazaList = []
    tipoCateringVsExtraAgendazaList = []
    variableEventoVsAExtraAgendaList = []

    def setEmpresaIds(self, empresaList):
        for item in empresaList:
            self.empresa_id_legacy_vs_agendaza_id[item.id_legacy] = item.id

