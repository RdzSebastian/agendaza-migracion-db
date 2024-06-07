class ForeignLegacyVsNewAux:
    empresa_id_legacy_vs_agendaza_id = {}

    variableCateringVsAExtraAgendaza = {}

    def setEmpresaIds(self, empresaList):
        for item in empresaList:
            self.empresa_id_legacy_vs_agendaza_id[item.id_legacy] = item.id

