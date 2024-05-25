from ETL.Conexión import conexionAgendaza
from ETL.Conexión import conexionGeserveApp
import pandas as pd
from ETL.gerservapp_legacy.Legacy import Legacy

conexionAgendaza.realizar_conexion()
conexionGeserveApp.realizar_conexion()

from repositorio.Repository import UsuarioLegacyRepository, Repositorio
from repositorio.UsuarioRepository import UsuarioRepository
from repositorio.ClienteRepository import ClienteLegacyRepository
from repositorio.EmpresaRepository import EmpresaRepository

usuarioLegacyRepository = UsuarioLegacyRepository(conexionGeserveApp.session)
usuarioAgendazaRepository = UsuarioRepository(conexionAgendaza.session)
clienteReseveappRepository = ClienteLegacyRepository(conexionGeserveApp.session)
empresaAgendazaAppRepository = EmpresaRepository(conexionAgendaza.session)
geserveAppQueries = Repositorio(conexionGeserveApp.session)  # Util cuando usamos nativeQuery
agendazaAppQueries = Repositorio(conexionAgendaza.session)  # Util cuando usamos nativeQuery

repositorioList = [usuarioLegacyRepository, usuarioAgendazaRepository, clienteReseveappRepository]

try:

    agendazaAppQueries.sqlNativeQuery("DELETE FROM CARGO where es_legacy IS TRUE")
    usuarioAgendazaRepository.sqlNativeQuery("DELETE FROM usuario where id_usuario_legacy IS NOT NULL")
    usuarioAgendazaRepository.sqlNativeQuery("DELETE FROM usuario where id_cliente_legacy IS NOT NULL")
    empresaAgendazaAppRepository.sqlNativeQuery("DELETE FROM empresa where id_legacy IS NOT NULL")

    usuarioAgendazaRepository.sqlNativeQuery("ALTER TABLE usuario DROP COLUMN IF EXISTS id_usuario_legacy")
    usuarioAgendazaRepository.sqlNativeQuery("ALTER TABLE usuario DROP COLUMN IF EXISTS id_cliente_legacy")
    usuarioLegacyRepository.sqlNativeQuery("ALTER TABLE usuario DROP COLUMN IF EXISTS id_agendaza")
    empresaAgendazaAppRepository.sqlNativeQuery("ALTER TABLE empresa DROP COLUMN IF EXISTS id_legacy")
    agendazaAppQueries.sqlNativeQuery("ALTER TABLE  CARGO DROP COLUMN   IF EXISTS es_legacy")
    geserveAppQueries.sqlNativeQuery("ALTER TABLE salon DROP COLUMN IF EXISTS  id_agendaza")

    idUsuarioMax = agendazaAppQueries.sqlNativeQuery("SELECT MAX(id)+1 FROM usuario").scalar()

    if idUsuarioMax is not None:
        agendazaAppQueries.sqlNativeQuery(f"ALTER SEQUENCE usuario_id_seq RESTART WITH {idUsuarioMax}")
    else:
        print("No se pudo obtener el valor de idUsuarioMax. No se reinició la secuencia.")

    idEmpresaMax = agendazaAppQueries.sqlNativeQuery("SELECT MAX(id)+1 FROM empresa").scalar()

    if idUsuarioMax is not None:
        agendazaAppQueries.sqlNativeQuery(f"ALTER SEQUENCE empresa_id_seq RESTART WITH {idEmpresaMax}")
    else:
        print("No se pudo obtener el valor de idEmpresaMax. No se reinició la secuencia.")


    idCargoMax = agendazaAppQueries.sqlNativeQuery("SELECT MAX(id)+1 FROM CARGO").scalar()

    if idUsuarioMax is not None:
        agendazaAppQueries.sqlNativeQuery(f"ALTER SEQUENCE cargo_id_seq RESTART WITH {idCargoMax}")
    else:
        print("No se pudo obtener el valor de idCargoMax. No se reinició la secuencia.")




except Exception as e:
    for repositorios in repositorioList:
        repositorios.rollback()

    print("No se puede descartar todos los cambios realizado por ETLScript debido a : ", e)

finally:
    conexionAgendaza.cerrar_conexion()
    conexionGeserveApp.cerrar_conexion()
