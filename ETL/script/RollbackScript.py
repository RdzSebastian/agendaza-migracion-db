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


class QueryDeleteyBase():
    repositorio = None
    query = None

    def __init__(self, repositorio: Repositorio, query: str):
        self.repositorio = repositorio
        self.query = query

    def borrarRegistros(self):
        try:
            self.repositorio.sqlNativeQuery(self.query)
        except Exception as e:
            print("No se puede descartar todos los cambios realizado por ETLScript debido a : ", e)


usuarioLegacyRepository = UsuarioLegacyRepository(conexionGeserveApp.session)
usuarioAgendazaRepository = UsuarioRepository(conexionAgendaza.session)
clienteReseveappRepository = ClienteLegacyRepository(conexionGeserveApp.session)
empresaAgendazaAppRepository = EmpresaRepository(conexionAgendaza.session)
geserveAppQueries = Repositorio(conexionGeserveApp.session)  # Util cuando usamos nativeQuery
agendazaAppQueries = Repositorio(conexionAgendaza.session)  # Util cuando usamos nativeQuery

repositorioList = [usuarioLegacyRepository, usuarioAgendazaRepository, clienteReseveappRepository]

try:

    queryDeleteFromList = []

    queryDeleteFromList.append(QueryDeleteyBase(agendazaAppQueries, "DELETE FROM CARGO where es_legacy IS TRUE"))
    queryDeleteFromList.append(
        QueryDeleteyBase(agendazaAppQueries, "DELETE FROM usuario where id_usuario_legacy IS NOT NULL"))
    queryDeleteFromList.append(
        QueryDeleteyBase(agendazaAppQueries, "DELETE FROM usuario where id_cliente_legacy IS NOT NULL"))
    queryDeleteFromList.append(QueryDeleteyBase(agendazaAppQueries,
                                                "DELETE FROM precio_con_fecha_extra WHERE  extra_variable_catering_legacy IS NOT NULL"))
    queryDeleteFromList.append(QueryDeleteyBase(agendazaAppQueries,
                                                "DELETE FROM precio_con_fecha_extra WHERE  extra_variable_sub_tipo_evento_legacy IS NOT NULL"))
    queryDeleteFromList.append(QueryDeleteyBase(agendazaAppQueries,
                                                "DELETE FROM precio_con_fecha_extra WHERE  extra_sub_tipo_evento_legacy IS NOT NULL"))
    queryDeleteFromList.append(QueryDeleteyBase(agendazaAppQueries,
                                                "DELETE FROM precio_con_fecha_extra WHERE  extra_tipo_catering_legacy IS NOT NULL"))
    queryDeleteFromList.append(
        QueryDeleteyBase(agendazaAppQueries, "DELETE FROM EXTRA where extra_variable_catering_id_legacy IS NOT NULL"))
    queryDeleteFromList.append(
        QueryDeleteyBase(agendazaAppQueries, "DELETE FROM EXTRA where tipo_catering_id_legacy IS NOT NULL"))
    queryDeleteFromList.append(
        QueryDeleteyBase(agendazaAppQueries, "DELETE FROM EXTRA where EXTRA_SUB_TIPO_EVENTO_ID_LEGACY IS NOT NULL"))
    queryDeleteFromList.append(QueryDeleteyBase(agendazaAppQueries,
                                                "DELETE FROM EXTRA where extra_variable_sub_tipo_evento_id_legacy IS NOT NULL"))
    queryDeleteFromList.append(QueryDeleteyBase(agendazaAppQueries, "DELETE FROM empresa where id_legacy IS NOT NULL"))


    for item in queryDeleteFromList:
        item.borrarRegistros()

    agendazaAppQueries.sqlNativeQuery(
        "ALTER TABLE  precio_con_fecha_extra DROP COLUMN   IF EXISTS extra_variable_catering_legacy")
    agendazaAppQueries.sqlNativeQuery(
        "ALTER TABLE  precio_con_fecha_extra DROP COLUMN   IF EXISTS extra_variable_sub_tipo_evento_legacy")
    agendazaAppQueries.sqlNativeQuery(
        "ALTER TABLE  precio_con_fecha_extra DROP COLUMN   IF EXISTS extra_sub_tipo_evento_legacy")
    agendazaAppQueries.sqlNativeQuery(
        "ALTER TABLE  precio_con_fecha_extra DROP COLUMN   IF EXISTS extra_tipo_catering_legacy")

    agendazaAppQueries.sqlNativeQuery("ALTER TABLE  EXTRA DROP COLUMN   IF EXISTS extra_variable_catering_id_legacy")
    agendazaAppQueries.sqlNativeQuery("ALTER TABLE  EXTRA DROP COLUMN   IF EXISTS EXTRA_SUB_TIPO_EVENTO_ID_LEGACY")
    agendazaAppQueries.sqlNativeQuery("ALTER TABLE  EXTRA DROP COLUMN   IF EXISTS tipo_catering_id_legacy")
    agendazaAppQueries.sqlNativeQuery(
        "ALTER TABLE  EXTRA DROP COLUMN  IF EXISTS extra_variable_sub_tipo_evento_id_legacy")

    agendazaAppQueries.sqlNativeQuery("ALTER TABLE usuario DROP COLUMN IF EXISTS id_usuario_legacy")
    agendazaAppQueries.sqlNativeQuery("ALTER TABLE usuario DROP COLUMN IF EXISTS id_cliente_legacy")
    geserveAppQueries.sqlNativeQuery("ALTER TABLE usuario DROP COLUMN IF EXISTS id_agendaza")
    agendazaAppQueries.sqlNativeQuery("ALTER TABLE empresa DROP COLUMN IF EXISTS id_legacy")
    agendazaAppQueries.sqlNativeQuery("ALTER TABLE  CARGO DROP COLUMN   IF EXISTS es_legacy")
    geserveAppQueries.sqlNativeQuery("ALTER TABLE salon DROP COLUMN IF EXISTS  id_agendaza")

    idUsuarioMax = agendazaAppQueries.sqlNativeQuery("SELECT MAX(id)+1 FROM usuario").scalar()

    if idUsuarioMax is not None:
        agendazaAppQueries.sqlNativeQuery(f"ALTER SEQUENCE usuario_id_seq RESTART WITH {idUsuarioMax}")
    else:
        print("No se pudo obtener el valor de idUsuarioMax. No se reinició la secuencia.")

    idEmpresaMax = agendazaAppQueries.sqlNativeQuery("SELECT MAX(id)+1 FROM empresa").scalar()

    if idEmpresaMax is not None:
        agendazaAppQueries.sqlNativeQuery(f"ALTER SEQUENCE empresa_id_seq RESTART WITH {idEmpresaMax}")
    else:
        print("No se pudo obtener el valor de idEmpresaMax. No se reinició la secuencia.")

    idCargoMax = agendazaAppQueries.sqlNativeQuery("SELECT MAX(id)+1 FROM CARGO").scalar()

    if idCargoMax is not None:
        agendazaAppQueries.sqlNativeQuery(f"ALTER SEQUENCE cargo_id_seq RESTART WITH {idCargoMax}")
    else:
        print("No se pudo obtener el valor de idCargoMax. No se reinició la secuencia.")

    idExtraMax = agendazaAppQueries.sqlNativeQuery("SELECT MAX(id)+1 FROM EXTRA").scalar()

    if idExtraMax is not None:
        agendazaAppQueries.sqlNativeQuery(f"ALTER SEQUENCE extra_id_seq RESTART WITH {idExtraMax}")
    else:
        print("No se pudo obtener el valor de idExtraMax. No se reinició la secuencia.")



except Exception as e:
    for repositorios in repositorioList:
        repositorios.rollback()

    print("No se puede descartar todos los cambios realizado por ETLScript debido a : ", e)

finally:
    conexionAgendaza.cerrar_conexion()
    conexionGeserveApp.cerrar_conexion()
