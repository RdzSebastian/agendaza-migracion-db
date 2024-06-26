from colorama import Fore
import logging


class InfoLog():

    numeroDeMigracion = 0


    async def expectativa(self, listaLegacy, repositorioActual, tablaLegacy, tablaAgendaza):

        self.numeroDeMigracion =self.numeroDeMigracion + 1
        self.log(f"{self.numeroDeMigracion}- MIGRACION DE {tablaLegacy}(GESERVAPP) -> ´{tablaAgendaza}(AGENDAZA) ",
                 Fore.GREEN)
        conteoAgendaza = await repositorioActual.count()
        mensaje = f'    {tablaLegacy}(GESERVAPP) : {len(listaLegacy)} REGISTROS'
        mensaje2 = f'    {tablaAgendaza}(AGENDAZA) : {conteoAgendaza} REGISTROS'
        suma = len(listaLegacy) + conteoAgendaza
        mensaje3 = f'    EXPECTATIVA : {suma} REGISTROS EN LA TABLA {tablaAgendaza} DE LA BD AGENDAZA'
        self.log(mensaje, Fore.CYAN)
        self.log(mensaje2, Fore.CYAN)
        self.log(mensaje3, Fore.MAGENTA)

    def log(self, mensaje, COLOR):
        print(f"{COLOR} {mensaje}{Fore.RESET}")

    async def validacionAgenda(self,conteoObtenido, listaAgendaza):
        conteoObtenido = int(conteoObtenido)
        suma = len(listaAgendaza)
        if conteoObtenido == suma:
            self.log(f'    RESULTADO : {conteoObtenido} - MIGRACION EXITOSA', Fore.LIGHTBLUE_EX)
        else:
            self.log(f'    RESULTADO : {conteoObtenido} - ERROR - REALIZAR ROLLBACK', Fore.LIGHTBLUE_EX)


class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.CYAN,  # Cyan para mensajes DEBUG
        'INFO': Fore.GREEN,  # Verde para mensajes INFO
        'WARNING': Fore.YELLOW,  # Amarillo para mensajes WARNING
        'ERROR': Fore.RED,  # Rojo para mensajes ERROR
        'CRITICAL': Fore.MAGENTA  # Magenta para mensajes CRITICAL
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, Fore.WHITE)  # Blanco para otros niveles
        log_msg = f"{log_color}{record.levelname}: {record.getMessage()}{Fore.RESET}"
        return log_msg
