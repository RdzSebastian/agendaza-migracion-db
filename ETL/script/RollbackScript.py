from ETL.Conexión import conexionAgendaza, conexionGeserveApp
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

    async def borrarRegistros(self):
        try:
            await self.repositorio.sqlNativeQuery(self.query)
        except Exception as e:
            print("No se puede descartar todos los cambios realizado por ETLScript debido a : ", e)


usuarioLegacyRepository = UsuarioLegacyRepository(conexionGeserveApp.session)
usuarioAgendazaRepository = UsuarioRepository(conexionAgendaza.session)
clienteReseveappRepository = ClienteLegacyRepository(conexionGeserveApp.session)
empresaAgendazaAppRepository = EmpresaRepository(conexionAgendaza.session)
geserveAppQueries = Repositorio(conexionGeserveApp.session)  # Util cuando usamos nativeQuery
agendazaAppQueries = Repositorio(conexionAgendaza.session)  # Util cuando usamos nativeQuery

repositorioList = [usuarioLegacyRepository, usuarioAgendazaRepository, clienteReseveappRepository]


async def main():
    try:
        queryDeleteFromList = []


        queryDeleteFromList.append(
            QueryDeleteyBase(agendazaAppQueries,
                             "DELETE FROM tipo_evento_extra where tipo_evento_id_legacy IS NOT NULL OR extra_tipo_catering_id_legacy IS NOT NULL OR extra_sub_tipo_evento_id_legacy IS NOT NULL or extra_sub_tipo_evento_variable_catering IS NOT NULL OR extra_sub_tipo_evento_extra_variable_catering IS NOT NULL"))

        queryDeleteFromList.append(
            QueryDeleteyBase(agendazaAppQueries,
                             "DELETE FROM evento_extra where evento_id_legacy IS NOT NULL OR extra_id_legacy IS NOT NULL"))

        queryDeleteFromList.append(
            QueryDeleteyBase(agendazaAppQueries,
                             "DELETE FROM evento_extra_variable where id_legacy IS NOT NULL"))

        queryDeleteFromList.append(
            QueryDeleteyBase(agendazaAppQueries,
                             "DELETE FROM tipo_evento_servicio where tipo_evento_id_legacy IS NOT NULL OR servicio_id_legacy IS NOT NULL"))

        queryDeleteFromList.append(
            QueryDeleteyBase(agendazaAppQueries, "DELETE FROM SERVICIO where servicio_id_legacy IS NOT NULL"))

        queryDeleteFromList.append(
            QueryDeleteyBase(agendazaAppQueries, "DELETE FROM PAGO where pago_id_legacy IS NOT NULL"))

        queryDeleteFromList.append(
            QueryDeleteyBase(agendazaAppQueries, "DELETE FROM EVENTO where evento_id_legacy IS NOT NULL"))

        queryDeleteFromList.append(
            QueryDeleteyBase(agendazaAppQueries, "DELETE FROM precio_con_fecha_tipo_evento where id_legacy IS NOT NULL"))

        queryDeleteFromList.append(
            QueryDeleteyBase(agendazaAppQueries, "DELETE FROM tipo_evento where tipo_evento_legacy IS NOT NULL"))

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

        queryDeleteFromList.append(QueryDeleteyBase(agendazaAppQueries, "DELETE FROM capacidad where es_migrado IS TRUE"))

        async def deleteQuerys():
            for item in queryDeleteFromList:
                await item.borrarRegistros()

        await deleteQuerys()

        async def alterTableQuerys():
            await agendazaAppQueries.sqlNativeQuery(
                "ALTER TABLE tipo_evento_extra DROP COLUMN IF EXISTS  tipo_evento_id_legacy")
            await agendazaAppQueries.sqlNativeQuery(
                "ALTER TABLE tipo_evento_extra DROP COLUMN IF EXISTS  extra_tipo_catering_id_legacy")
            await agendazaAppQueries.sqlNativeQuery(
                "ALTER TABLE tipo_evento_extra DROP COLUMN IF EXISTS  extra_sub_tipo_evento_id_legacy")
            await agendazaAppQueries.sqlNativeQuery(
                "ALTER TABLE tipo_evento_extra DROP COLUMN IF EXISTS  extra_sub_tipo_evento_variable_catering")
            await agendazaAppQueries.sqlNativeQuery(
                "ALTER TABLE tipo_evento_extra DROP COLUMN IF EXISTS  extra_sub_tipo_evento_extra_variable_catering")
            await agendazaAppQueries.sqlNativeQuery("ALTER TABLE evento_extra DROP COLUMN IF EXISTS  evento_id_legacy")
            await agendazaAppQueries.sqlNativeQuery("ALTER TABLE evento_extra DROP COLUMN IF EXISTS  extra_id_legacy")
            await agendazaAppQueries.sqlNativeQuery(
                "ALTER TABLE evento_extra_variable DROP COLUMN IF EXISTS  id_legacy")
            await agendazaAppQueries.sqlNativeQuery(
                "ALTER TABLE tipo_evento_servicio DROP COLUMN IF EXISTS  tipo_evento_id_legacy")
            await agendazaAppQueries.sqlNativeQuery(
                "ALTER TABLE tipo_evento_servicio DROP COLUMN IF EXISTS  servicio_id_legacy")
            await agendazaAppQueries.sqlNativeQuery("ALTER TABLE SERVICIO DROP COLUMN IF EXISTS  servicio_id_legacy")
            await agendazaAppQueries.sqlNativeQuery("ALTER TABLE PAGO DROP COLUMN IF EXISTS  pago_id_legacy")
            await agendazaAppQueries.sqlNativeQuery("ALTER TABLE  EVENTO  DROP COLUMN  IF EXISTS evento_id_legacy")
            await agendazaAppQueries.sqlNativeQuery(
                "ALTER TABLE  precio_con_fecha_tipo_evento DROP COLUMN  IF EXISTS id_legacy")
            await agendazaAppQueries.sqlNativeQuery(
                "ALTER TABLE  tipo_evento DROP COLUMN  IF EXISTS tipo_evento_legacy")
            await agendazaAppQueries.sqlNativeQuery(
                "ALTER TABLE  precio_con_fecha_extra DROP COLUMN   IF EXISTS extra_variable_catering_legacy")
            await agendazaAppQueries.sqlNativeQuery(
                "ALTER TABLE  precio_con_fecha_extra DROP COLUMN   IF EXISTS extra_variable_sub_tipo_evento_legacy")
            await agendazaAppQueries.sqlNativeQuery(
                "ALTER TABLE  precio_con_fecha_extra DROP COLUMN   IF EXISTS extra_sub_tipo_evento_legacy")
            await agendazaAppQueries.sqlNativeQuery(
                "ALTER TABLE  precio_con_fecha_extra DROP COLUMN   IF EXISTS extra_tipo_catering_legacy")
            await agendazaAppQueries.sqlNativeQuery(
                "ALTER TABLE  EXTRA DROP COLUMN   IF EXISTS extra_variable_catering_id_legacy")
            await agendazaAppQueries.sqlNativeQuery(
                "ALTER TABLE  EXTRA DROP COLUMN   IF EXISTS EXTRA_SUB_TIPO_EVENTO_ID_LEGACY")
            await agendazaAppQueries.sqlNativeQuery(
                "ALTER TABLE  EXTRA DROP COLUMN   IF EXISTS tipo_catering_id_legacy")
            await agendazaAppQueries.sqlNativeQuery(
                "ALTER TABLE  EXTRA DROP COLUMN  IF EXISTS extra_variable_sub_tipo_evento_id_legacy")
            await agendazaAppQueries.sqlNativeQuery("ALTER TABLE usuario DROP COLUMN IF EXISTS id_usuario_legacy")
            await agendazaAppQueries.sqlNativeQuery("ALTER TABLE usuario DROP COLUMN IF EXISTS id_cliente_legacy")
            await geserveAppQueries.sqlNativeQuery("ALTER TABLE usuario DROP COLUMN IF EXISTS id_agendaza")
            await agendazaAppQueries.sqlNativeQuery("ALTER TABLE empresa DROP COLUMN IF EXISTS id_legacy")
            await agendazaAppQueries.sqlNativeQuery("ALTER TABLE  CARGO DROP COLUMN   IF EXISTS es_legacy")
            await geserveAppQueries.sqlNativeQuery("ALTER TABLE salon DROP COLUMN IF EXISTS  id_agendaza")
            await agendazaAppQueries.sqlNativeQuery("ALTER TABLE capacidad DROP COLUMN IF EXISTS  es_migrado")

        await alterTableQuerys()

        async def reset_sequence_if_max_value_exists(table_name, sequence_name, query_instance):
            max_id_query = f"SELECT MAX(id)+1 FROM {table_name}"
            max_id = (await query_instance.sqlNativeQuery(max_id_query)).scalar()
            if max_id is not None:
                await query_instance.sqlNativeQuery(f"ALTER SEQUENCE {sequence_name} RESTART WITH {max_id}")
            else:
                print(f"No se pudo obtener el valor máximo de ID para {table_name}. No se reinició la secuencia.")

        # Lista de tablas y secuencias
        tables_sequences = [
            ("usuario", "usuario_id_seq"),
            ("empresa", "empresa_id_seq"),
            ("cargo", "cargo_id_seq"),
            ("extra", "extra_id_seq"),
            ("precio_con_fecha_extra", "precio_con_fecha_extra_id_seq"),
            ("capacidad", "capacidad_id_seq"),
            ("tipo_evento", "tipo_evento_id_seq"),
            ("precio_con_fecha_tipo_evento", "precio_con_fecha_tipo_evento_id_seq"),
            ("evento", "evento_id_seq"),
            ("servicio", "servicio_id_seq"),
            ("evento_extra_variable", "evento_extra_variable_id_seq")
        ]

        # Iterar sobre cada tabla y secuencia para reiniciar si es posible
        for table, sequence in tables_sequences:
            await reset_sequence_if_max_value_exists(table, sequence, agendazaAppQueries)

    except Exception as e:
        for repositorio in repositorioList:
            await repositorio.rollback()

        print("No se puede descartar todos los cambios realizado por ETLScript debido a : ", e)

    finally:
        conexionAgendaza.cerrar_conexion()
        conexionGeserveApp.cerrar_conexion()


import asyncio

asyncio.run(main())
