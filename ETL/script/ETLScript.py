from ETL.Conexión import conexionAgendaza
from ETL.Conexión import conexionGeserveApp
import pandas as pd
from ETL.gerservapp_legacy.Legacy import Legacy


# Solo usarlo para probar que se hayan traido los datos desde la  desde la BD
# EJEMPLO -> visualizar(usuarioLegacyList) donde  usuarioLegacyList es una lista de usuariosLegacy extraido desde la BD utilizando
# sqlalchemy como ORM
def visualizar(obj):
    data = [{key: value for key, value in vars(item).items() if key != '_sa_instance_state'} for item in obj]
    df = pd.DataFrame(data)
    print(df)


##Solo los objetos que heredan de Legacy pueden transformarse
def transformacion(obj: Legacy):
    listaARetornar = []
    for item in obj:
        listaARetornar.append(item.conversion())

    return listaARetornar


def columnasAuxiliares():
    global usuarioLegacyRepository
    global usuarioAgendazaRepository
    usuarioAgendazaRepository.sqlNativeQuery("ALTER TABLE usuario ADD COLUMN id_legacy INTEGER unique ")
    usuarioLegacyRepository.sqlNativeQuery("ALTER TABLE usuario ADD COLUMN id_agendaza INTEGER unique")


def ETLUsuario():
    global usuarioLegacyRepository
    global usuarioAgendazaRepository

    # EXTRACCION
    usuarioLegacyList = usuarioLegacyRepository.getAll()
    # TRANSFORMACION
    usuarioAgendazaList = transformacion(usuarioLegacyList)
    # LOAD/CARGA/MIGRACION -> ETL Finalizado
    usuarioAgendazaRepository.saveAll(usuarioAgendazaList)

    # Solo por las dudas
    for item in usuarioLegacyList:
        item.asignarIdAgendaza()

    usuarioLegacyRepository.saveAll(usuarioLegacyList)


def ETLCliente():
    global clienteRepository
    global usuarioAgendazaRepository




conexionAgendaza.realizar_conexion()
conexionGeserveApp.realizar_conexion()

from repositorio.Repository import UsuarioLegacyRepository
from repositorio.UsuarioRepository import UsuarioRepository
from repositorio.ClienteRepository import ClienteLegacyRepository

clienteRepository = ClienteLegacyRepository(conexionGeserveApp.Session)
usuarioLegacyRepository = UsuarioLegacyRepository(conexionGeserveApp.Session)
usuarioAgendazaRepository = UsuarioRepository(conexionAgendaza.Session)

columnasAuxiliares()
ETLUsuario()

conexionAgendaza.cerrar_conexion()
conexionGeserveApp.cerrar_conexion()
