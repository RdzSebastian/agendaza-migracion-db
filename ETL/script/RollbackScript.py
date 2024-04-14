from ETL.Conexión import conexionAgendaza
from ETL.Conexión import conexionGeserveApp
import pandas as pd
from ETL.gerservapp_legacy.Legacy import Legacy

conexionAgendaza.realizar_conexion()
conexionGeserveApp.realizar_conexion()

from repositorio.Repository import UsuarioLegacyRepository
from repositorio.UsuarioRepository import UsuarioRepository
from repositorio.ClienteRepository import ClienteLegacyRepository

usuarioLegacyRepository = UsuarioLegacyRepository(conexionGeserveApp.session)
usuarioAgendazaRepository = UsuarioRepository(conexionAgendaza.session)
clienteRepository = ClienteLegacyRepository(conexionGeserveApp.session)

repositorioList = [usuarioLegacyRepository, usuarioAgendazaRepository, clienteRepository]

try:
    usuarioAgendazaRepository.sqlNativeQuery("DELETE FROM usuario where id_usuario_legacy IS NOT NULL")
    usuarioAgendazaRepository.sqlNativeQuery("ALTER TABLE usuario DROP COLUMN IF EXISTS id_usuario_legacy")
    usuarioLegacyRepository.sqlNativeQuery("ALTER TABLE usuario DROP COLUMN IF EXISTS id_agendaza")
except Exception as e:
    for repositorios in repositorioList:
        repositorios.rollback()
    print("No se puede descartar todos los cambios realizado por ETLScript debido a : ", e)
finally:
    conexionAgendaza.cerrar_conexion()
    conexionGeserveApp.cerrar_conexion()
