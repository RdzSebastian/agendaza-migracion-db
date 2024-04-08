from util.Configuracion import Configuracion
from model.geserveapp.UsuarioLegacy import UsuarioLegacy

class Migracion:
    configuracion = None

    def __init__(self, configuracion: Configuracion):
        self.configuracion = configuracion

    def realizarMigracion(self):
        usuarioRepositorio = self.configuracion.usuario_elegacy_repositorio
        ##Test
        user1 = UsuarioLegacy(nombre='Mauricio',
                              apellido='Martinez',
                              username='TheMauricio',
                              password='adasfasfasf',
                              mail='mauricio@mail.com',
                              account_non_expired=False,
                              account_non_locked=True,
                              credentials_non_expired=True,
                              enabled=True)

        usuarioRepositorio.save(user1)


configuracion = Configuracion()
configuracion.inicializar()
migracion = Migracion(configuracion)
##migracion.realizarMigracion()