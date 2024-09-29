from colorama import Fore
import logging
import time


class InfoLog():
    numeroDeMigracion = 0
    inicio = None
    parcial = None
    fin = None

    def iniciarTiempo(self):
        self.inicio = time.time()
        self.parcial = time.time()

    def finalizarTiempo(self):
        self.fin = time.time()

    def tiempoDeEjecucion(self):

        tiempo_ejecucion = self.fin - self.inicio

        minutos = int(tiempo_ejecucion // 60)
        segundos = int(tiempo_ejecucion % 60)
        self.log(f"SE HA TARDADO = {minutos:02}:{segundos:02} EN MIGRAR TODOS LOS DATOS", Fore.LIGHTRED_EX)

    async def expectativa(self, listaLegacy, repositorioActual, tablaLegacy, tablaAgendaza):

        self.numeroDeMigracion = self.numeroDeMigracion + 1
        self.log(
            f"{self.numeroDeMigracion}- MIGRACION DE {Fore.LIGHTYELLOW_EX}{tablaLegacy}{Fore.GREEN}(GESERVAPP) -> {Fore.LIGHTYELLOW_EX}{tablaAgendaza}{Fore.GREEN}(AGENDAZA)",
            Fore.GREEN
        )
        conteoAgendaza = await repositorioActual.count()
        mensaje = f'    {tablaLegacy}(GESERVAPP) : {len(listaLegacy)} REGISTROS'
        mensaje2 = f'    {tablaAgendaza}(AGENDAZA) : {conteoAgendaza} REGISTROS'
        suma = len(listaLegacy) + conteoAgendaza
        mensaje3 = f'    EXPECTATIVA : {suma} REGISTROS EN LA TABLA {tablaAgendaza} DE LA BD AGENDAZA'
        self.log(mensaje, Fore.CYAN)
        self.log(mensaje2, Fore.CYAN)
        self.log(mensaje3, Fore.MAGENTA)

        return suma

    async def expectativa2(self, listaLegacy, conteoAgendaza, tablaLegacy, tablaAgendaza):

        counLegacy = listaLegacy
        counLegacy = len(counLegacy)

        self.numeroDeMigracion = self.numeroDeMigracion + 1
        self.log(
            f"{self.numeroDeMigracion}- MIGRACION DE {Fore.LIGHTYELLOW_EX}{tablaLegacy}{Fore.GREEN}(GESERVAPP) -> {Fore.LIGHTYELLOW_EX}{tablaAgendaza}{Fore.GREEN}(AGENDAZA)",
            Fore.GREEN
        )
        conteoAgendaza = conteoAgendaza
        mensaje = f'    {tablaLegacy}(GESERVAPP) : {counLegacy} REGISTROS'
        mensaje2 = f'    {tablaAgendaza}(AGENDAZA) : {conteoAgendaza} REGISTROS'
        suma = counLegacy + conteoAgendaza
        mensaje3 = f'    EXPECTATIVA : {suma} REGISTROS EN LA TABLA {tablaAgendaza} DE LA BD AGENDAZA'
        self.log(mensaje, Fore.CYAN)
        self.log(mensaje2, Fore.CYAN)
        self.log(mensaje3, Fore.MAGENTA)

        return suma

    async def expectativas(self, conteoLegacyList, conteoAgendaza, tablaLegacy, tablaAgendaza):
        pass
        # conteoLegacy = len(list(conteoLegacyList))

    def log(self, mensaje, COLOR):
        print(f"{COLOR} {mensaje}{Fore.RESET}")

    async def resultadoValidacion(self, conteoObtenido, conteoAgendaza):

        conteoObtenido = int(conteoObtenido)
        suma = int(conteoAgendaza)

        tiempo_ejecucion = time.time() - self.parcial

        minutos = int(tiempo_ejecucion // 60)
        segundos = int(tiempo_ejecucion % 60)

        if conteoObtenido == suma:
            self.log(f'    RESULTADO : {conteoAgendaza} - MIGRACION EXITOSA', Fore.LIGHTBLUE_EX)
            self.log(f"TIEMPO DEL ETL = {minutos:02}:{segundos:02}", Fore.RESET)
            self.parcial = time.time()
        else:
            self.log(f'    RESULTADO : {conteoAgendaza} - ERROR - REALIZAR ROLLBACK', Fore.RED)


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
