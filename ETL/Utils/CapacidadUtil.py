class CapacidadUtil:
    capacidadAgendazaList = []


    def obtenerCombinacionesQueNoExistenEnAgendaza(self, capacidadAgendazaList, capacidadLegacyList):

        capacidadesAMigrar = []

        for capLegacy in capacidadLegacyList:
            if not self.laCombinacionExisteEnAgendaza(capacidadAgendazaList, capLegacy):
                capLegacy.es_migrado = True
                capacidadesAMigrar.append(capLegacy)

        return capacidadesAMigrar

    def laCombinacionExisteEnAgendaza(self, capacidadAgendazaList, combinacion):

        for capacidad in capacidadAgendazaList:
            if combinacion.capacidad_adultos == capacidad.capacidad_adultos and combinacion.capacidad_ninos == capacidad.capacidad_ninos:
                return True

        return False

    def generarDiccionarioIdLegacyIdAgendaza(self, capacidadesLegacy):

        dicARetornar = {}

        for capacidadLegacy in capacidadesLegacy:
            idAgendaza = self.determinarElIdActualEnAgendaza(
                capacidadLegacy)

            dicARetornar[capacidadLegacy.id] = idAgendaza

        return dicARetornar

    def determinarElIdActualEnAgendaza(self, capacidadLegacy):

        for capacidadAgendaza in self.capacidadAgendazaList:
            if capacidadAgendaza.capacidad_adultos == capacidadLegacy.capacidad_adultos and capacidadAgendaza.capacidad_ninos == capacidadLegacy.capacidad_ninos:

                return capacidadAgendaza.id

