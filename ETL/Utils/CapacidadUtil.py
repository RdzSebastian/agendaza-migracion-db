class CapacidadUtil:

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
