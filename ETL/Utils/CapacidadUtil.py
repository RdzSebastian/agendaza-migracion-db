class CapacidadUtil:
    capacidadAgendazaList = []

    capacidadLegacyCapacidadAgendazaDic = {}

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

        for capacidadLegacy in capacidadesLegacy:
            idAgendaza = self.determinarElIdActualEnAgendaza(
                capacidadLegacy)
            print(capacidadLegacy.id ,idAgendaza )

            self.capacidadLegacyCapacidadAgendazaDic[capacidadLegacy.id] = idAgendaza

        print(self.capacidadLegacyCapacidadAgendazaDic)

    def determinarElIdActualEnAgendaza(self, capacidadLegacy):

        for capacidadAgendaza in self.capacidadAgendazaList:
            if capacidadAgendaza.capacidad_adultos == capacidadLegacy.capacidad_adultos and capacidadAgendaza.capacidad_ninos == capacidadLegacy.capacidad_ninos:

                return capacidadAgendaza.id

    def obtenerCapacidadAgendaza(self,idLegacy):
        return self.capacidadLegacyCapacidadAgendazaDic.get(idLegacy)
