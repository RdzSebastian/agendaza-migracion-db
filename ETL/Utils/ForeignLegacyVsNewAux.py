class ForeignLegacyVsNewAux:
    empresa_id_legacy_vs_agendaza_id = {}
    usuario_id_legacy_vs_agendaza_id = {}
    cliente_id_legacy_vs_agendaza_id = {}
    evento_id_legacy_vs_agendaza_id = {}
    servicio_id_legacy_vs_agendaza_id = {}


    variableCateringVsAExtraAgendazaList = []
    subTipoEventoVsAExtraAgendazaList = []
    tipoCateringVsExtraAgendazaList = []
    variableEventoVsAExtraAgendaList = []
    capacidadIdLegacyCapacidadIdAgendazaDic = {}
    tipoEventoIdLegacyTipoEventoIdAgendazaDic = {}

    extra_tipo_catering_id_legacy_vs_agendaza_id = {}
    extra_variable_evento_id_legacy_vs_agendaza_id = {}
    extra_sub_tipo_evento_id_legacy_vs_agendaza_id = {}
    extra_variable_catering_id_legacy_vs_agendaza_id = {}

    extra_tipo_table = {
        "VARIABLE_CATERING" : "VARIABLE_CATERING",
        "EVENTO" : "SUB_TIPO_EVENTO",
        "TIPO_CATERING" : "TIPO_CATERING",
        "VARIABLE_EVENTO" : "VARIABLE_SUB_TIPO_EVENTO",
    }

    precio_con_fecha_hora_Table = {
        "VARIABLE_CATERING" : "PRECIO_CON_FECHA_HORA_EXTRA_VARIABLE_CATERING",
        "EVENTO" : "PRECIO_CON_FECHA_HORA_EXTRA_SUB_TIPO_EVENTO",
        "TIPO_CATERING" : "PRECIO_CON_FECHA_HORA_EXTRA_TIPO_CATERING",
        "VARIABLE_EVENTO" : "PRECIO_CON_FECHA_HORA_EXTRA_VARIABLE_SUB_TIPO_EVENTO",
    }

    evento_Extra_table = {
        "TIPO_CATERING" : "SUB_TIPO_EVENTO_TIPO_CATERING",
        "EVENTO" : "SUB_TIPO_EVENTO_EXTRA",
        "VARIABLE_EVENTO" : "SUB_TIPO_EVENTO_EXTRA_VARIABLE",
        "VARIABLE_CATERING" : "SUB_TIPO_EVENTO_EXTRA_VARIABLE",
    }




    def setEmpresaIds(self, empresaList):
        for item in empresaList:
            self.empresa_id_legacy_vs_agendaza_id[item.id_legacy] = item.id

    #Mal planteado pero aun asi funciona y lo hace de manera exelente.
    # Los diccionarios fueron mejor solucion pero se  pensaron e implementaron muy tarde
    #Los diccionarios mencionados son
    # extra_tipo_catering_id_legacy_vs_agendaza_id = {}
    #extra_variable_evento_id_legacy_vs_agendaza_id = {}
    # extra_sub_tipo_evento_id_legacy_vs_agendaza_id = {}
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

    def obtenerFKExtraSegunIdLegacy(self, tipo, id):
        if tipo == "VARIABLE_CATERING":
            return self.extra_variable_catering_id_legacy_vs_agendaza_id.get(id)
        if tipo == "EVENTO":
            return self.extra_sub_tipo_evento_id_legacy_vs_agendaza_id.get(id)

        if tipo == "TIPO_CATERING":
            return self.extra_tipo_catering_id_legacy_vs_agendaza_id.get(id)

        if tipo == "VARIABLE_EVENTO":
            return self.extra_variable_evento_id_legacy_vs_agendaza_id.get(id)

