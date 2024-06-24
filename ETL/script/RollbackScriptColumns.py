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

    agendazaAppQueries.sqlNativeQuery("ALTER TABLE tipo_evento_extra DROP COLUMN IF EXISTS  tipo_evento_id_legacy")
    agendazaAppQueries.sqlNativeQuery(
        "ALTER TABLE tipo_evento_extra DROP COLUMN IF EXISTS  extra_tipo_catering_id_legacy")

    agendazaAppQueries.sqlNativeQuery(
        "ALTER TABLE tipo_evento_extra DROP COLUMN IF EXISTS  extra_sub_tipo_evento_id_legacy")

    agendazaAppQueries.sqlNativeQuery(
        "ALTER TABLE tipo_evento_extra DROP COLUMN IF EXISTS  extra_sub_tipo_evento_variable_catering")

    agendazaAppQueries.sqlNativeQuery(
        "ALTER TABLE tipo_evento_extra DROP COLUMN IF EXISTS  extra_sub_tipo_evento_extra_variable_catering")

    agendazaAppQueries.sqlNativeQuery("ALTER TABLE evento_extra DROP COLUMN IF EXISTS  evento_id_legacy")
    agendazaAppQueries.sqlNativeQuery("ALTER TABLE evento_extra DROP COLUMN IF EXISTS  extra_id_legacy")
    agendazaAppQueries.sqlNativeQuery("ALTER TABLE evento_extra_variable DROP COLUMN IF EXISTS  id_legacy")
    agendazaAppQueries.sqlNativeQuery("ALTER TABLE tipo_evento_servicio DROP COLUMN IF EXISTS  tipo_evento_id_legacy")
    agendazaAppQueries.sqlNativeQuery("ALTER TABLE tipo_evento_servicio DROP COLUMN IF EXISTS  servicio_id_legacy")

    agendazaAppQueries.sqlNativeQuery("ALTER TABLE SERVICIO DROP COLUMN IF EXISTS  servicio_id_legacy")

    agendazaAppQueries.sqlNativeQuery("ALTER TABLE PAGO DROP COLUMN IF EXISTS  pago_id_legacy")

    agendazaAppQueries.sqlNativeQuery(
        "ALTER TABLE  EVENTO  DROP COLUMN  IF EXISTS evento_id_legacy")

    agendazaAppQueries.sqlNativeQuery(
        "ALTER TABLE  precio_con_fecha_tipo_evento DROP COLUMN  IF EXISTS id_legacy")

    agendazaAppQueries.sqlNativeQuery(
        "ALTER TABLE  tipo_evento DROP COLUMN  IF EXISTS tipo_evento_legacy")

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
    agendazaAppQueries.sqlNativeQuery("ALTER TABLE capacidad DROP COLUMN IF EXISTS  es_migrado")





except Exception as e:
    for repositorios in repositorioList:
        repositorios.rollback()

    print("No se puede descartar todos los cambios realizado por ETLScript debido a : ", e)

finally:
    conexionAgendaza.cerrar_conexion()
    conexionGeserveApp.cerrar_conexion()
