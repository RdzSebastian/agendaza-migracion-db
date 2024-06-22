class ForeignLegacyVsNewAux:
    empresa_id_legacy_vs_agendaza_id = {}
    usuario_id_legacy_vs_agendaza_id = {}
    cliente_id_legacy_vs_agendaza_id = {}
    evento_id_legacy_vs_agendaza_id = {}
    servicio_id_legacy_vs_agendaza_id = {}
    extra_variable_evento_id_legacy_vs_agendaza_id = {}
    extra_sub_tipo_evento_id_legacy_vs_agendaza_id = {}

    variableCateringVsAExtraAgendazaList = []
    subTipoEventoVsAExtraAgendazaList = []
    tipoCateringVsExtraAgendazaList = []
    variableEventoVsAExtraAgendaList = []
    capacidadIdLegacyCapacidadIdAgendazaDic = {}
    tipoEventoIdLegacyTipoEventoIdAgendazaDic = {}


    def setEmpresaIds(self, empresaList):
        for item in empresaList:
            self.empresa_id_legacy_vs_agendaza_id[item.id_legacy] = item.id

    def obtenerFKS(self, empresa_id_legacy, extra_id_legacy, tipo):
        empresa_id_retorno = None
        extra_id_retorno = None
        listaARecorrer = None
        if tipo == "VARIABLE_CATERING":
            listaARecorrer = self.variableCateringVsAExtraAgendazaList

        if tipo == "EVENTO":
            listaARecorrer = self.subTipoEventoVsAExtraAgendazaList

        if tipo == "TIPO_CATERING":
            listaARecorrer = self.tipoCateringVsExtraAgendazaList

        if tipo == "VARIABLE_EVENTO":
            listaARecorrer = self.variableEventoVsAExtraAgendaList

        for item in listaARecorrer:
            if item.cumpleParaPrecioExtra(empresa_id_legacy, extra_id_legacy):
                empresa_id_retorno = item.id_empresa
                extra_id_retorno = item.id_agendaza

        return empresa_id_retorno, extra_id_retorno

    def obtenerFkCapacidadAgendaza(self, idLegacy):
        return self.capacidadIdLegacyCapacidadIdAgendazaDic.get(idLegacy)

    def obtenerFkEmpresaAgendaza(self,idLegacy):
        return self.empresa_id_legacy_vs_agendaza_id.get(idLegacy)
