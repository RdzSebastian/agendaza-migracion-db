from colorama import Fore
from sqlalchemy.orm.base import PASSIVE_OFF

from ETL.Conexión import conexionAgendaza
from ETL.Conexión import conexionGeserveApp
import pandas as pd

from ETL.Utils.CapacidadUtil import CapacidadUtil
from ETL.Utils.ForeignLegacyVsNewAux import ForeignLegacyVsNewAux
from ETL.Utils.InfoLog import InfoLog
from ETL.Utils.NativeQuerys import NativeQuerys
from ETL.Utils.ExtraGeserveAppVsExtraAgendaza import ExtraGeserveAppVsExtraAgendaza
from ETL.gerservapp_legacy.Legacy import Legacy

import asyncio

import logging


# Ejemplo de uso


# Solo usarlo para probar que se hayan traído los datos desde la BD
# EJEMPLO -> visualizar(usuarioLegacyList) donde usuarioLegacyList es una lista de usuariosLegacy extraído desde la BD utilizando
# sqlalchemy como ORM
def visualizar(obj):
    data = [{key: value for key, value in vars(item).items() if key != '_sa_instance_state'} for item in obj]
    df = pd.DataFrame(data)
    print(df)


## Solo los objetos que heredan de Legacy pueden transformarse
def transformacion(obj: Legacy):
    listaARetornar = []
    for item in obj:
        listaARetornar.append(item.conversion())

    return listaARetornar


async def columnasAuxiliares():
    global usuarioLegacyRepository
    global usuarioAgendazaRepository
    global clienteReserveappRepository
    global empresaAgendazaAppRepository

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

    await usuarioAgendazaRepository.sqlNativeQuery("ALTER TABLE usuario ADD COLUMN id_usuario_legacy INTEGER unique");
    await usuarioAgendazaRepository.sqlNativeQuery("ALTER TABLE usuario ADD COLUMN id_cliente_legacy INTEGER unique");
    await usuarioLegacyRepository.sqlNativeQuery("ALTER TABLE usuario ADD COLUMN id_agendaza INTEGER unique");
    await empresaAgendazaAppRepository.sqlNativeQuery("ALTER TABLE empresa ADD COLUMN id_legacy INTEGER unique");
    await cargoRepository.sqlNativeQuery("ALTER TABLE cargo ADD COLUMN es_legacy BOOLEAN");
    await geserveAppQueries.sqlNativeQuery("ALTER TABLE salon ADD COLUMN id_agendaza INTEGER unique");
    await agendazaAppQueries.sqlNativeQuery("ALTER TABLE extra ADD COLUMN extra_variable_catering_id_legacy INTEGER");
    await agendazaAppQueries.sqlNativeQuery("ALTER TABLE extra ADD COLUMN EXTRA_SUB_TIPO_EVENTO_ID_LEGACY INTEGER");
    await agendazaAppQueries.sqlNativeQuery("ALTER TABLE extra ADD COLUMN tipo_catering_id_legacy INTEGER");
    await agendazaAppQueries.sqlNativeQuery(
        "ALTER TABLE extra ADD COLUMN extra_variable_sub_tipo_evento_id_legacy INTEGER");

    await agendazaAppQueries.sqlNativeQuery(
        "ALTER TABLE precio_con_fecha_extra ADD COLUMN extra_variable_catering_legacy INTEGER");
    await agendazaAppQueries.sqlNativeQuery(
        "ALTER TABLE precio_con_fecha_extra ADD COLUMN extra_variable_sub_tipo_evento_legacy INTEGER");
    await agendazaAppQueries.sqlNativeQuery(
        "ALTER TABLE precio_con_fecha_extra ADD COLUMN extra_sub_tipo_evento_legacy INTEGER");
    await agendazaAppQueries.sqlNativeQuery(
        "ALTER TABLE precio_con_fecha_extra ADD COLUMN extra_tipo_catering_legacy INTEGER");

    await agendazaAppQueries.sqlNativeQuery("ALTER TABLE capacidad ADD COLUMN es_migrado BOOLEAN");

    await agendazaAppQueries.sqlNativeQuery("ALTER TABLE tipo_evento ADD COLUMN tipo_evento_legacy INTEGER");

    await agendazaAppQueries.sqlNativeQuery("ALTER TABLE precio_con_fecha_tipo_evento ADD COLUMN id_legacy INTEGER");

    await agendazaAppQueries.sqlNativeQuery("ALTER TABLE EVENTO ADD COLUMN evento_id_legacy INTEGER");

    await agendazaAppQueries.sqlNativeQuery("ALTER TABLE PAGO ADD COLUMN pago_id_legacy INTEGER");

    await agendazaAppQueries.sqlNativeQuery("ALTER TABLE SERVICIO ADD COLUMN servicio_id_legacy INTEGER");

    await agendazaAppQueries.sqlNativeQuery(
        "ALTER TABLE tipo_evento_servicio ADD COLUMN tipo_evento_id_legacy INTEGER");
    await agendazaAppQueries.sqlNativeQuery("ALTER TABLE tipo_evento_servicio ADD COLUMN servicio_id_legacy INTEGER");

    await agendazaAppQueries.sqlNativeQuery("ALTER TABLE evento_extra_variable ADD COLUMN id_legacy INTEGER");
    await agendazaAppQueries.sqlNativeQuery("ALTER TABLE evento_extra ADD COLUMN evento_id_legacy INTEGER");
    await agendazaAppQueries.sqlNativeQuery("ALTER TABLE evento_extra ADD COLUMN extra_id_legacy INTEGER");

    await agendazaAppQueries.sqlNativeQuery("ALTER TABLE TIPO_EVENTO_EXTRA ADD COLUMN tipo_evento_id_legacy INTEGER");
    await agendazaAppQueries.sqlNativeQuery(
        "ALTER TABLE TIPO_EVENTO_EXTRA ADD COLUMN extra_tipo_catering_id_legacy INTEGER");
    await agendazaAppQueries.sqlNativeQuery(
        "ALTER TABLE TIPO_EVENTO_EXTRA ADD COLUMN extra_sub_tipo_evento_id_legacy INTEGER");

    await agendazaAppQueries.sqlNativeQuery(
        "ALTER TABLE TIPO_EVENTO_EXTRA ADD COLUMN extra_sub_tipo_evento_variable_catering INTEGER");

    await agendazaAppQueries.sqlNativeQuery(
        "ALTER TABLE TIPO_EVENTO_EXTRA ADD COLUMN extra_sub_tipo_evento_extra_variable_catering INTEGER");

    await agendazaAppQueries.sqlNativeQuery(
        "ALTER TABLE EMPRESA_SERVICIO ADD COLUMN empresa_id_legacy INTEGER");

    await agendazaAppQueries.sqlNativeQuery(
        "ALTER TABLE EMPRESA_SERVICIO ADD COLUMN servicio_id_legacy INTEGER");


async def ETLUsuario():
    global usuarioLegacyRepository
    global usuarioAgendazaRepository

    # EXTRACCION
    usuarioLegacyList = await  usuarioLegacyRepository.getAll()

    conteo = await infoLog.expectativa(usuarioLegacyList, usuarioAgendazaRepository, 'USUARIO', 'USUARIO')

    # TRANSFORMACION
    usuarioAgendazaList = transformacion(usuarioLegacyList)
    # LOAD/CARGA/MIGRACION -> ETL Finalizado
    await usuarioAgendazaRepository.saveAll(usuarioAgendazaList)

    # Solo por las dudas
    for item in usuarioLegacyList:
        item.asignarIdAgendaza()

    await usuarioLegacyRepository.saveAll(usuarioLegacyList)
    await postUsuarioETL(usuarioAgendazaList)

    await infoLog.resultadoValidacion(conteo, await usuarioAgendazaRepository.count())


async def postUsuarioETL(usuarioAgendazaList):
    global foreignLegacyVsNewAux

    for usuarioMigrado in usuarioAgendazaList:
        foreignLegacyVsNewAux.usuario_id_legacy_vs_agendaza_id[usuarioMigrado.id_usuario_legacy] = usuarioMigrado.id


async def ETLCliente():
    global clienteReserveappRepository
    global usuarioAgendazaRepository

    # Extraccion
    clienteLegacyList = await clienteReserveappRepository.getAll()

    conteo = await infoLog.expectativa(clienteLegacyList, usuarioAgendazaRepository, 'CLIENTE', 'USUARIO')

    # TRANSFORMACION
    usuarioAgendazaList = transformacion(clienteLegacyList)

    # LOAD/CARGA/MIGRACION -> ETL Finalizado
    await usuarioAgendazaRepository.saveAll(usuarioAgendazaList)
    await postClienteETL(usuarioAgendazaList)

    await infoLog.resultadoValidacion(conteo, await usuarioAgendazaRepository.count())


async def postClienteETL(usuarioAgendazaList):
    global foreignLegacyVsNewAux

    for usuarioItem in usuarioAgendazaList:
        foreignLegacyVsNewAux.cliente_id_legacy_vs_agendaza_id[usuarioItem.id_cliente_legacy] = usuarioItem.id


# print("KEY CLIENTE ID_LEGACY - VALUE USUARIO_ID_AGENDAZA",
#      foreignLegacyVsNewAux.cliente_id_legacy_vs_agendaza_id)


async def ETLEmpresa():
    global salonLegacyRepository
    global empresaAgendazaAppRepository
    salones = await salonLegacyRepository.getAll()
    listaEmpresa = transformacion(salones)

    conteo = await infoLog.expectativa(salones, empresaAgendazaAppRepository, 'SALON', 'EMPRESA')

    await empresaAgendazaAppRepository.saveAll(listaEmpresa)

    for item in salones:
        item.asignarIdAgendaza()

    await salonLegacyRepository.saveAll(salones)
    await infoLog.resultadoValidacion(conteo, await empresaAgendazaAppRepository.count())

    return listaEmpresa


async def cargoETL2():
    global geserveAppQueries
    global nativeQuerys
    global foreignLegacyVsNewAux
    global cargoRepository
    cargoLegacyList = list(await geserveAppQueries.sqlNativeQuery(nativeQuerys.queryForCargoETL))
    listaAMigrar = []
    conteo = await infoLog.expectativa2(cargoLegacyList, await cargoRepository.count(), 'ROL', 'CARGO')

    for cargoLeg in cargoLegacyList:
        usuario_id = foreignLegacyVsNewAux.usuario_id_legacy_vs_agendaza_id.get(cargoLeg.usuario_id)
        empresa_id = foreignLegacyVsNewAux.empresa_id_legacy_vs_agendaza_id.get(cargoLeg.empresa_id)
        cargoAMigrar = Cargo(
            usuario_id=usuario_id,
            tipo_cargo=cargoLeg.tipo_cargo
        )

        cargoAMigrar.empresa_id = empresa_id
        cargoAMigrar.es_legacy = True

        listaAMigrar.append(cargoAMigrar)

    await cargoRepository.saveAll(listaAMigrar)

    await infoLog.resultadoValidacion(conteo, await cargoRepository.count())


async def extraETL(query, foreignLegacyVsNewAux, tipo):
    global extraRepository

    extraList = list(await geserveAppQueries.sqlNativeQuery(query))
    empresa_id_id_legacy = foreignLegacyVsNewAux.empresa_id_legacy_vs_agendaza_id
    extraReturn = []

    conteo = await infoLog.expectativa2(extraList, await extraRepository.count(),
                                        foreignLegacyVsNewAux.extra_tipo_table.get(tipo), "EXTRA")

    for row in extraList:
        extra = Extra(nombre=row.nombre, tipo_extra=tipo)
        extra.empresa_id = empresa_id_id_legacy.get(row.empresa_id)
        await definirQueIdSetear(extra, row.id)
        extraReturn.append(extra)
        await extraRepository.save(extra)
        await setNewforeignLegacyVsNewAux(extra, row.id, row.empresa_id)

    await infoLog.resultadoValidacion(conteo, await extraRepository.count())


async def duplicarExtrasMigradosParaEmpresaDiferente():
    global extraRepository
    global nativeQuerys

    listaDeExtrasNoDuplicadas = list(await extraRepository.sqlNativeQuery(
        nativeQuerys.queryForExtrasMigradosNoDuplicadosAgendaza))

    valores = foreignLegacyVsNewAux.empresa_id_legacy_vs_agendaza_id.values()

    conteo = await infoLog.expectativa2(listaDeExtrasNoDuplicadas, await extraRepository.count(),
                                        "EXTRAS LEGACY SIN DUPLICAR EN EL OTRO SALON", "EXTRA")

    listaADeNuevosExtrasPorDuplicacion = []

    for extra in listaDeExtrasNoDuplicadas:
        listaDeEmpresa_Id = list(valores)
        listaDeEmpresa_Id.remove(extra.empresa_id)

        for valor in listaDeEmpresa_Id:
            nuevoExtra = Extra(nombre=extra.nombre, tipo_extra=extra.tipo_extra)
            nuevoExtra.empresa_id = valor

            nuevoExtra.extra_variable_catering_id_legacy = extra.extra_variable_catering_id_legacy
            nuevoExtra.extra_sub_tipo_evento_id_legacy = extra.extra_sub_tipo_evento_id_legacy
            nuevoExtra.tipo_catering_id_legacy = extra.tipo_catering_id_legacy
            nuevoExtra.extra_variable_sub_tipo_evento_id_legacy = extra.extra_variable_sub_tipo_evento_id_legacy

            listaADeNuevosExtrasPorDuplicacion.append(nuevoExtra)

    await extraRepository.saveAll(listaADeNuevosExtrasPorDuplicacion)
    await infoLog.resultadoValidacion(conteo, await extraRepository.count())


async def precioConFechaExtraETL(repository, tipo):
    global foreignLegacyVsNewAux
    global precioConFechaExtraRepository
    precioConHoraLegacy = list(await repository.getAll())

    precioConHoraAgendazaList = []
    conteo = await infoLog.expectativa2(precioConHoraLegacy, await precioConFechaExtraRepository.count(),
                                        foreignLegacyVsNewAux.precio_con_fecha_hora_Table.get(tipo),
                                        "PRECIO_CON_FECHA_HORA", )

    for precioConHora in precioConHoraLegacy:
        empresa_id, extra_id = foreignLegacyVsNewAux.obtenerFKS(precioConHora.salon_id, precioConHora.idLegacy(), tipo)
        precioConHora.empresa_id = empresa_id
        precioConHora.extra_id = extra_id
        precioConFechaHoraAgendaza = precioConHora.conversion()
        precioConHoraAgendazaList.append(precioConFechaHoraAgendaza)

    await precioConFechaExtraRepository.saveAll(precioConHoraAgendazaList)
    await infoLog.resultadoValidacion(conteo, await precioConFechaExtraRepository.count())


async def definirQueIdSetear(extra, id):
    if extra.tipo_extra == "VARIABLE_CATERING":
        extra.extra_variable_catering_id_legacy = id

    if extra.tipo_extra == "EVENTO":
        extra.extra_sub_tipo_evento_id_legacy = id

    if extra.tipo_extra == "TIPO_CATERING":
        extra.tipo_catering_id_legacy = id

    if extra.tipo_extra == "VARIABLE_EVENTO":
        extra.extra_variable_sub_tipo_evento_id_legacy = id


async def setNewforeignLegacyVsNewAux(extra, idLegacy, empresaLegacyId):
    global foreignLegacyVsNewAux
    idVsIdLegacy = None
    if extra.tipo_extra == "VARIABLE_CATERING":
        idVsIdLegacy = ExtraGeserveAppVsExtraAgendaza(id_agendaza=extra.id, id_legacy=idLegacy,
                                                      id_empresa=extra.empresa_id,
                                                      id_empresa_legacy=empresaLegacyId
                                                      )

        foreignLegacyVsNewAux.variableCateringVsAExtraAgendazaList.append(idVsIdLegacy)
        foreignLegacyVsNewAux.extra_variable_catering_id_legacy_vs_agendaza_id[idLegacy] = extra.id

    if extra.tipo_extra == "EVENTO":
        idVsIdLegacy = ExtraGeserveAppVsExtraAgendaza(id_agendaza=extra.id, id_legacy=idLegacy,
                                                      id_empresa=extra.empresa_id,
                                                      id_empresa_legacy=empresaLegacyId
                                                      )

        foreignLegacyVsNewAux.subTipoEventoVsAExtraAgendazaList.append(idVsIdLegacy)
        foreignLegacyVsNewAux.extra_sub_tipo_evento_id_legacy_vs_agendaza_id[idLegacy] = extra.id

    if extra.tipo_extra == "TIPO_CATERING":
        idVsIdLegacy = ExtraGeserveAppVsExtraAgendaza(id_agendaza=extra.id, id_legacy=idLegacy,
                                                      id_empresa=extra.empresa_id,
                                                      id_empresa_legacy=empresaLegacyId
                                                      )

        foreignLegacyVsNewAux.tipoCateringVsExtraAgendazaList.append(idVsIdLegacy)
        foreignLegacyVsNewAux.extra_tipo_catering_id_legacy_vs_agendaza_id[idLegacy] = extra.id

    if extra.tipo_extra == "VARIABLE_EVENTO":
        idVsIdLegacy = ExtraGeserveAppVsExtraAgendaza(id_agendaza=extra.id, id_legacy=idLegacy,
                                                      id_empresa=extra.empresa_id,
                                                      id_empresa_legacy=empresaLegacyId
                                                      )

        foreignLegacyVsNewAux.variableEventoVsAExtraAgendaList.append(idVsIdLegacy)
        foreignLegacyVsNewAux.extra_variable_evento_id_legacy_vs_agendaza_id[
            extra.extra_variable_sub_tipo_evento_id_legacy] = extra.id


async def capacidadETL():
    global capacidadRepository
    global nativeQuerys
    global geserveAppQueries
    capacidadListAgendaza = await capacidadRepository.getAll()
    global capacidadUtil

    capacidadListGeserveApp = list(await geserveAppQueries.sqlNativeQuery(nativeQuerys.queryForCapacidadGeserveApp))

    capacidadLegacyTransformed = []

    for row in capacidadListGeserveApp:
        capacidadLegacy = Capacidad(capacidad_adultos=row.capacidad_adultos,
                                    capacidad_ninos=row.capacidad_ninos)
        capacidadLegacyTransformed.append(capacidadLegacy)

    capacidadAMigrar = capacidadUtil.obtenerCombinacionesQueNoExistenEnAgendaza(capacidadListAgendaza,
                                                                                capacidadLegacyTransformed)

    conteo = await infoLog.expectativa2(capacidadAMigrar, await capacidadRepository.count(), "CAPACIDAD",
                                        "CAPACIDAD")

    await capacidadRepository.saveAll(capacidadAMigrar)

    await postMigracionCapacidadETL(capacidadListAgendaza, capacidadAMigrar)
    await infoLog.resultadoValidacion(conteo, await capacidadRepository.count())


async def postMigracionCapacidadETL(capacidadListAgendaza, capacidadAMigrar):
    global capacidadRepository
    global nativeQuerys
    global geserveAppQueries
    global capacidadUtil
    global foreignLegacyVsNewAux

    capacidadUtil.capacidadAgendazaList = capacidadListAgendaza

    for cap in capacidadAMigrar:
        capacidadUtil.capacidadAgendazaList.append(cap)

    todasLasCapacidades = await geserveAppQueries.sqlNativeQuery(
        nativeQuerys.queryForCapacidadGeserveAppFullPostMigration)

    todasLasCapacidadesLegacyTransformadas = []

    for row in todasLasCapacidades:
        capacidadLegacy = Capacidad(capacidad_adultos=row.capacidad_adultos,
                                    capacidad_ninos=row.capacidad_ninos)
        capacidadLegacy.id = row.id
        todasLasCapacidadesLegacyTransformadas.append(capacidadLegacy)

    dic = capacidadUtil.generarDiccionarioIdLegacyIdAgendaza(todasLasCapacidadesLegacyTransformadas)
    foreignLegacyVsNewAux.capacidadIdLegacyCapacidadIdAgendazaDic = dic


async def tipoEventoETL():
    global nativeQuerys
    global geserveAppQueries
    global capacidadUtil
    global foreignLegacyVsNewAux
    global tipoEventoRepository
    listaDeTipoEventosLegacy = list(await geserveAppQueries.sqlNativeQuery(nativeQuerys.querySubTipoEventoLegacy))

    conteo = await infoLog.expectativa2(listaDeTipoEventosLegacy, await tipoEventoRepository.count(), "SUB_TIPO_EVENTO",
                                        "TIPO_EVENTO")

    listaAMigrar = []

    for tipoEventoLegacy in listaDeTipoEventosLegacy:
        tipoEvento = TipoEvento(nombre=tipoEventoLegacy.nombre,
                                duracion=tipoEventoLegacy.duracion,
                                capacidad_id=foreignLegacyVsNewAux.obtenerFkCapacidadAgendaza(
                                    tipoEventoLegacy.capacidad_id),
                                cantidad_duracion=tipoEventoLegacy.cantidad_duracion,
                                empresa_id=foreignLegacyVsNewAux.obtenerFkEmpresaAgendaza(tipoEventoLegacy.empresa_id))

        tipoEvento.tipo_evento_legacy = tipoEventoLegacy.id

        listaAMigrar.append(tipoEvento)

    await tipoEventoRepository.saveAll(listaAMigrar)
    await postTipoEventoETL(listaAMigrar)
    await infoLog.resultadoValidacion(conteo, await tipoEventoRepository.count())


async def postTipoEventoETL(listaTipoEventos):
    global foreignLegacyVsNewAux

    for tipoEventoMigrado in listaTipoEventos:
        foreignLegacyVsNewAux.tipoEventoIdLegacyTipoEventoIdAgendazaDic[
            tipoEventoMigrado.tipo_evento_legacy] = tipoEventoMigrado.id


async def precioConFechaEventoRepositoryETL():
    global nativeQuerys
    global geserveAppQueries
    global foreignLegacyVsNewAux
    global precioConFechaEventoRepository

    listaDeFechaEventoLegacyRepository = list(await geserveAppQueries.sqlNativeQuery(
        nativeQuerys.queryForPrecioConFechaSubTipoEventoGeserveApp))

    conteo = await infoLog.expectativa2(listaDeFechaEventoLegacyRepository,
                                        await precioConFechaEventoRepository.count(),
                                        "PRECIO_CON_FECHA_SUB_TIPO_EVENTO", "PRECIO_CON_FECHA_EVENTO")

    lista_a_migrar = []

    for fechaEventoLegacy in listaDeFechaEventoLegacyRepository:
        empresa_id = foreignLegacyVsNewAux.empresa_id_legacy_vs_agendaza_id.get(fechaEventoLegacy.empresa_id)
        tipo_evento_id = foreignLegacyVsNewAux.tipoEventoIdLegacyTipoEventoIdAgendazaDic.get(
            fechaEventoLegacy.tipo_evento_id)

        precioConFechaEventoAMigrar = PrecioConFechaEvento(
            desde=fechaEventoLegacy.desde
            , hasta=fechaEventoLegacy.hasta,
            precio=fechaEventoLegacy.precio,
            empresa_id=empresa_id,
            tipo_evento_id=tipo_evento_id
        )

        precioConFechaEventoAMigrar.id_legacy = fechaEventoLegacy.id
        lista_a_migrar.append(precioConFechaEventoAMigrar)
    await precioConFechaEventoRepository.saveAll(lista_a_migrar)
    await infoLog.resultadoValidacion(conteo, await precioConFechaEventoRepository.count())


async def eventoETL():
    global foreignLegacyVsNewAux
    global geserveAppQueries
    global nativeQuerys
    global eventoRepository

    eventosLegacyList = list(await  geserveAppQueries.sqlNativeQuery(nativeQuerys.queryForEvento))
    eventosAMigrar = []

    conteo = await infoLog.expectativa2(eventosLegacyList, await eventoRepository.count(), "EVENTO", "EVENTO")

    for eventoLegacy in eventosLegacyList:
        capacidad_id = foreignLegacyVsNewAux.capacidadIdLegacyCapacidadIdAgendazaDic.get(eventoLegacy.capacidad_id)
        cliente_id = foreignLegacyVsNewAux.cliente_id_legacy_vs_agendaza_id.get(eventoLegacy.cliente_id)
        empresa_id = foreignLegacyVsNewAux.empresa_id_legacy_vs_agendaza_id.get(eventoLegacy.empresa_id)
        encargado_id = foreignLegacyVsNewAux.usuario_id_legacy_vs_agendaza_id.get(eventoLegacy.encargado_id)
        tipo_evento_id = foreignLegacyVsNewAux.tipoEventoIdLegacyTipoEventoIdAgendazaDic.get(
            eventoLegacy.tipo_evento_id)

        eventoAMigrar = Evento(
            catering_otro=eventoLegacy.catering_otro,
            codigo=eventoLegacy.codigo,
            descuento=eventoLegacy.descuento,
            estado="RESERVADO",
            extra_otro=eventoLegacy.extra_otro,
            fin=eventoLegacy.fin,
            inicio=eventoLegacy.inicio,
            nombre=eventoLegacy.nombre,
            capacidad_id=capacidad_id,
            cliente_id=cliente_id,
            empresa_id=empresa_id,
            encargado_id=encargado_id,
            tipo_evento_id=tipo_evento_id,
            evento_id_legacy=eventoLegacy.id
        )

        eventosAMigrar.append(eventoAMigrar)

    await eventoRepository.saveAll(eventosAMigrar)
    await postEventoETL(eventosAMigrar)
    await infoLog.resultadoValidacion(conteo, await eventoRepository.count())


async def postEventoETL(listaDeEventosMigrados):
    global foreignLegacyVsNewAux

    for eventoMigrado in listaDeEventosMigrados:
        foreignLegacyVsNewAux.evento_id_legacy_vs_agendaza_id[eventoMigrado.evento_id_legacy] = eventoMigrado.id


# print("KEY EVENTO ID_LEGACY - VALUE EVENTO ID AGENDAZA : ", foreignLegacyVsNewAux.evento_id_legacy_vs_agendaza_id)


async def pagoETL():
    global geserveAppQueries
    global pagoRepository
    global nativeQuerys
    global foreignLegacyVsNewAux

    listaDePagosLegacy = list(await geserveAppQueries.sqlNativeQuery(nativeQuerys.queryForPago))
    listaAMigrar = []

    conteo = await infoLog.expectativa2(listaDePagosLegacy, await pagoRepository.count(), "PAGO", "PAGO")

    for pagoLegacy in listaDePagosLegacy:
        encargado_id = foreignLegacyVsNewAux.usuario_id_legacy_vs_agendaza_id.get(pagoLegacy.encargado_id)
        evento_id = foreignLegacyVsNewAux.evento_id_legacy_vs_agendaza_id.get(pagoLegacy.evento_id)

        pagoAMigrar = Pago(
            fecha=pagoLegacy.fecha,
            medio_de_pago=pagoLegacy.medio_de_pago,
            monto=pagoLegacy.monto,
            encargado_id=encargado_id,
            evento_id=evento_id,
            pago_id_legacy=pagoLegacy.id,

        )
        pagoAMigrar.correccionMedioDePago()

        listaAMigrar.append(pagoAMigrar)

    await pagoRepository.saveAll(listaAMigrar)


async def servicioETL():
    global geserveAppQueries
    global servicioRepository
    global nativeQuerys
    global foreignLegacyVsNewAux

    listaDeServiciosLegacy = list(await geserveAppQueries.sqlNativeQuery(nativeQuerys.queryForServicio))
    listaDeServiciosAMigrar = []

    conteo = await infoLog.expectativa2(listaDeServiciosLegacy, await servicioRepository.count(), "SERVICIO",
                                        "SERVICIO")

    for servicioLegacy in listaDeServiciosLegacy:
        empresa_id = foreignLegacyVsNewAux.empresa_id_legacy_vs_agendaza_id.get(servicioLegacy.empresa_id)

        servicioAMigrar = Servicio(fecha_baja=None,
                                   empresa_id=empresa_id,
                                   nombre=servicioLegacy.nombre,
                                   servicio_id_legacy=servicioLegacy.id
                                   )

        listaDeServiciosAMigrar.append(servicioAMigrar)

    await servicioRepository.saveAll(listaDeServiciosAMigrar)

    await postServicioETL(listaDeServiciosAMigrar)
    await infoLog.resultadoValidacion(conteo, await servicioRepository.count())


async def postServicioETL(serviciosMigrados):
    global foreignLegacyVsNewAux

    for servicioMigrado in serviciosMigrados:
        foreignLegacyVsNewAux.servicio_id_legacy_vs_agendaza_id[servicioMigrado.servicio_id_legacy] = servicioMigrado.id

    # print("KEY SERVICIO ID_LEGACY - VALUE EVENTO ID AGENDAZA : ",
    #     foreignLegacyVsNewAux.servicio_id_legacy_vs_agendaza_id)


async def tipoEventoServicioETL():
    global geserveAppQueries
    global tipoEventoServicioRepository
    global nativeQuerys
    global foreignLegacyVsNewAux

    listaTipoEventoServicioLegacy = list(
        await geserveAppQueries.sqlNativeQuery(nativeQuerys.queryForSubTipoEventoServicio))
    listaTipoEventoServiciosAMigrar = []

    conteo = await infoLog.expectativa2(listaTipoEventoServicioLegacy, await tipoEventoServicioRepository.count(),
                                        "SUB_TIPO_EVENTO_SERVICIO", "TIPO_EVENTO_SERVICIO")

    for tipoEventoServicioLegacy in listaTipoEventoServicioLegacy:
        tipo_evento_id = foreignLegacyVsNewAux.tipoEventoIdLegacyTipoEventoIdAgendazaDic.get(
            tipoEventoServicioLegacy.tipo_evento_id)
        servicio_id = foreignLegacyVsNewAux.servicio_id_legacy_vs_agendaza_id.get(tipoEventoServicioLegacy.servicio_id)
        tipoEventoServicioLegacyAMigrar = TipoEventoServicio(tipo_evento_id=tipo_evento_id,
                                                             servicio_id=servicio_id,
                                                             tipo_evento_id_legacy=tipoEventoServicioLegacy.tipo_evento_id,
                                                             servicio_id_legacy=tipoEventoServicioLegacy.servicio_id)
        listaTipoEventoServiciosAMigrar.append(tipoEventoServicioLegacyAMigrar)

    await tipoEventoServicioRepository.saveAll(listaTipoEventoServiciosAMigrar)

    await infoLog.resultadoValidacion(conteo, await tipoEventoServicioRepository.count())


async def eventoExtraVariable():
    global geserveAppQueries
    global nativeQuerys
    global foreignLegacyVsNewAux
    global eventoExtraVariableRepository

    listaEventoExtraVaraibleLegacy = list(
        await  geserveAppQueries.sqlNativeQuery(nativeQuerys.queryForEventoExtraVariable))

    conteo = await infoLog.expectativa2(listaEventoExtraVaraibleLegacy, await eventoExtraVariableRepository.count(),
                                        "EVENTO_EXTRA_VARIABLE_SUB_TIPO_EVENTO", "EVENTO_EXTRA_VARIABLE")

    listaEventoExtraVariableAMigrar = []

    for eventoExtraVariableLegacy in listaEventoExtraVaraibleLegacy:
        evento_id = foreignLegacyVsNewAux.evento_id_legacy_vs_agendaza_id.get(eventoExtraVariableLegacy.evento_id)
        extra_id = foreignLegacyVsNewAux.extra_variable_evento_id_legacy_vs_agendaza_id.get(
            eventoExtraVariableLegacy.extra_id)

        eventoExtraVariableLegacyAMigrar = EventoExtraVariable(cantidad=eventoExtraVariableLegacy.cantidad,
                                                               evento_id=evento_id,
                                                               extra_id=extra_id,
                                                               id_legacy=eventoExtraVariableLegacy.id)

        listaEventoExtraVariableAMigrar.append(eventoExtraVariableLegacyAMigrar)

    await eventoExtraVariableRepository.saveAll(listaEventoExtraVariableAMigrar)
    await infoLog.resultadoValidacion(conteo, await eventoExtraVariableRepository.count())


async def eventoExtraETL():
    global geserveAppQueries
    global nativeQuerys
    global foreignLegacyVsNewAux
    global eventoExtraRepository

    listaEventoExtraLegacyAMigrar = list(await geserveAppQueries.sqlNativeQuery(
        nativeQuerys.queryForEventoExtraSubTipoEvento))

    conteo = await  infoLog.expectativa2(listaEventoExtraLegacyAMigrar, await eventoExtraRepository.count(),
                                         "EVENTO_EXTRA_SUB_TIPO_EVENTO", "EVENTO_EXTRA")

    listaAMigrar = []

    for eventoExtraLegacy in listaEventoExtraLegacyAMigrar:
        evento_id = foreignLegacyVsNewAux.evento_id_legacy_vs_agendaza_id.get(eventoExtraLegacy.evento_id)
        extra_id = foreignLegacyVsNewAux.extra_sub_tipo_evento_id_legacy_vs_agendaza_id.get(eventoExtraLegacy.extra_id)

        eventoExtraAMigrar = EventoExtra(evento_id=evento_id, extra_id=extra_id,
                                         evento_id_legacy=eventoExtraLegacy.evento_id,
                                         extra_id_legacy=eventoExtraLegacy.extra_id)
        listaAMigrar.append(eventoExtraAMigrar)

    await eventoExtraRepository.saveAll(listaAMigrar)
    await infoLog.resultadoValidacion(conteo, await eventoExtraRepository.count())


async def tipoEventoExtraETL(query, tipo):
    global geserveAppQueries
    global nativeQuerys
    global foreignLegacyVsNewAux
    global tipoEventoExtraRepository

    listaAMigrar = list(await geserveAppQueries.sqlNativeQuery(query))

    conteo = await infoLog.expectativa2(listaAMigrar, await tipoEventoExtraRepository.count(),
                                        foreignLegacyVsNewAux.evento_Extra_table.get(tipo), "TIPO_EVENTO")
    listaAGuardar = []

    for tipoEventoExtraLegacy in listaAMigrar:
        tipo_evento_id = foreignLegacyVsNewAux.tipoEventoIdLegacyTipoEventoIdAgendazaDic.get(
            tipoEventoExtraLegacy.tipo_evento_id)

        extra_id = foreignLegacyVsNewAux.obtenerFKExtraSegunIdLegacy(tipo, tipoEventoExtraLegacy.extra_id)

        tipoEventoExtraLegacyAMigrar = TipoEventoExtra(tipo_evento_id=tipo_evento_id,
                                                       tipo_evento_id_legacy=tipoEventoExtraLegacy.tipo_evento_id,
                                                       extra_id=extra_id)

        tipoEventoExtraLegacyAMigrar.asignarIdLegacy(tipo, tipoEventoExtraLegacy.extra_id)
        listaAGuardar.append(tipoEventoExtraLegacyAMigrar)

    await tipoEventoExtraRepository.saveAll(listaAGuardar)
    await infoLog.resultadoValidacion(conteo, await tipoEventoExtraRepository.count())


async def servicioETLV2():
    global geserveAppQueries
    global servicioRepository
    global nativeQuerys
    global foreignLegacyVsNewAux

    listaDeServiciosLegacy = list(await geserveAppQueries.sqlNativeQuery(nativeQuerys.queryForServicioV2))
    listaDeServiciosAMigrar = []

    conteo = await infoLog.expectativa2(listaDeServiciosLegacy, await servicioRepository.count(), "SERVICIO",
                                        "SERVICIO")

    for servicioLegacy in listaDeServiciosLegacy:
        servicioAMigrar = Servicio(fecha_baja=None,
                                   nombre=servicioLegacy.nombre,
                                   servicio_id_legacy=servicioLegacy.id
                                   )

        listaDeServiciosAMigrar.append(servicioAMigrar)

    await servicioRepository.saveAll(listaDeServiciosAMigrar)
    await postServicioETL(listaDeServiciosAMigrar)
    await infoLog.resultadoValidacion(conteo, await servicioRepository.count())


async def empresaServicioETL():
    global geserveAppQueries
    global empresaServicioRepository
    global nativeQuerys
    listaDeEmpresaServiciosLegacy = list(
        await geserveAppQueries.sqlNativeQuery(nativeQuerys.queryForEmpresaServicioGeserveApp))
    listaDeEmpresaServiciosAMigrar = []

    print("EMPRESA_SERVICIO_LEGACY COUNT", len(listaDeEmpresaServiciosLegacy))

    conteo = await infoLog.expectativa2(listaDeEmpresaServiciosLegacy, await empresaServicioRepository.count(),
                                        "SERVICIO JOIN SUB_TIPO_EVENTO_SERVICIO JOIN SUB_TIPO_EVENTO JOIN PRECIO_CON_FECHA_SUB_TIPO_EVENTO",
                                        "EMPRESA_SERVICIO")
    # foreignLegacyVsNewAux.servicio_id_legacy_vs_agendaza_id[servicioMigrado.servicio_id_legacy] = servicioMigrado.id
    for item in listaDeEmpresaServiciosLegacy:
        empresa_id = foreignLegacyVsNewAux.empresa_id_legacy_vs_agendaza_id.get(item.empresa_id)
        servicio_id = foreignLegacyVsNewAux.servicio_id_legacy_vs_agendaza_id.get(item.servicio_id)
        empresa_servicio_a_migrar = EmpresaServicio(
            empresa_id=empresa_id,
            servicio_id=servicio_id,
            empresa_id_legacy=item.empresa_id,
            servicio_id_legacy=item.servicio_id
        )

        listaDeEmpresaServiciosAMigrar.append(empresa_servicio_a_migrar)

    await empresaServicioRepository.saveAll(listaDeEmpresaServiciosAMigrar)
    await infoLog.resultadoValidacion(conteo, await empresaServicioRepository.count())


##############################################################################################################
async def main():
    global foreignLegacyVsNewAux
    global nativeQuerys
    global precioConFechaExtraVariableCateringRepository
    global precioConFechaExtraSubTipoEventoRepository
    global precioConFechaExtraTipoCateringRepository
    global precioConFechaExtraVariableEventoRepository

    infoLog.iniciarTiempo()
    await columnasAuxiliares()
    await ETLUsuario()
    await ETLCliente()
    listaEmpresa = await ETLEmpresa()
    foreignLegacyVsNewAux.setEmpresaIds(listaEmpresa)

    await cargoETL2()
    await extraETL(nativeQuerys.queryVARIABLE_CATERING, foreignLegacyVsNewAux, "VARIABLE_CATERING")
    await extraETL(nativeQuerys.queryExtSubTipoEvento, foreignLegacyVsNewAux, "EVENTO")
    await extraETL(nativeQuerys.queryTipoCatering, foreignLegacyVsNewAux, "TIPO_CATERING")
    await extraETL(nativeQuerys.queryVariable_Evento, foreignLegacyVsNewAux, "VARIABLE_EVENTO")
    await duplicarExtrasMigradosParaEmpresaDiferente()
    await precioConFechaExtraETL(precioConFechaExtraVariableCateringRepository, "VARIABLE_CATERING")
    await precioConFechaExtraETL(precioConFechaExtraSubTipoEventoRepository, "EVENTO")
    await precioConFechaExtraETL(precioConFechaExtraTipoCateringRepository, "TIPO_CATERING")
    await precioConFechaExtraETL(precioConFechaExtraVariableEventoRepository, "VARIABLE_EVENTO")
    await capacidadETL()
    await tipoEventoETL()
    await precioConFechaEventoRepositoryETL()
    await eventoETL()
    await pagoETL()
    await servicioETLV2()
    await tipoEventoServicioETL()
    await eventoExtraVariable()
    await eventoExtraETL()
    await tipoEventoExtraETL(nativeQuerys.queryForSubTipoEventoTipoCatering, "TIPO_CATERING")
    await tipoEventoExtraETL(nativeQuerys.queryFroSubTipoEvento, "EVENTO")
    await tipoEventoExtraETL(nativeQuerys.queryForSubTipoEventoExtraVariable, "VARIABLE_EVENTO")
    await tipoEventoExtraETL(nativeQuerys.queryForSubTipoEventoExtraVariableCatering, "VARIABLE_CATERING")
    await empresaServicioETL()
    infoLog.finalizarTiempo()
    infoLog.tiempoDeEjecucion()

    conexionAgendaza.cerrar_conexion()
    conexionGeserveApp.cerrar_conexion()


conexionAgendaza.realizar_conexion()
conexionGeserveApp.realizar_conexion()

from repositorio.Repository import UsuarioLegacyRepository
from repositorio.UsuarioRepository import UsuarioRepository
from repositorio.ClienteRepository import ClienteLegacyRepository
from repositorio.EmpresaRepository import EmpresaRepository
from ETL.agendaza.Empresa import Empresa
from ETL.agendaza.Cargo import Cargo
from repositorio.Repository import Repositorio
from repositorio.CargoRepository import CargoRepository
from repositorio.SalonLegacyRepositorio import SalonLegacyRepositorio
from repositorio.ExtraRepository import ExtraRepository
from ETL.agendaza.Extra import Extra
from repositorio.PrecioConFechaExtraRepository import PrecioConFechaExtraVariableCateringRepository, \
    PrecioConFechaExtraSubTipoEventoRepository, PrecioConFechaExtraTipoCateringRepository, \
    PrecioConFechaExtraVariableEventoRepository, PrecioConFechaExtraRepository

from repositorio.CapacidadRepository import CapacidadRepository
from ETL.agendaza.Capacidad import Capacidad
from ETL.agendaza.TipoEvento import TipoEvento

from repositorio.TipoEventoRepository import TipoEventoRepository
from repositorio.PrecioConFechaEventoRepository import PrecioConFechaEventoRepository
from ETL.agendaza.PrecioConFechaEvento import PrecioConFechaEvento
from repositorio.EventoRepository import EventoRepository
from ETL.agendaza.Evento import Evento
from repositorio.PagoRepository import PagoRepository
from ETL.agendaza.Pago import Pago
from repositorio.ServicioRepository import ServicioRepository
from ETL.agendaza.Servicio import Servicio
from repositorio.TipoEventoServicioRepository import TipoEventoServicioRepository
from ETL.agendaza.TipoEventoServicio import TipoEventoServicio
from repositorio.EventoExtraVariableRepository import EventoExtraVariableRepository
from ETL.agendaza.EventoExtraVariable import EventoExtraVariable
from repositorio.EventoExtraRepository import EventoExtraRepository
from ETL.agendaza.EventoExtra import EventoExtra
from repositorio.TipoEventoExtraRepository import TipoEventoExtraRepository
from ETL.agendaza.TipoEventoExtra import TipoEventoExtra
from repositorio.EmpresaServicioRepository import EmpresaServicioRepository
from ETL.agendaza.EmpresaServicio import EmpresaServicio

usuarioLegacyRepository = UsuarioLegacyRepository(conexionGeserveApp.session)
usuarioAgendazaRepository = UsuarioRepository(conexionAgendaza.session)
clienteReserveappRepository = ClienteLegacyRepository(conexionGeserveApp.session)
empresaGeserveAppRepository = EmpresaRepository(conexionGeserveApp.session)
empresaAgendazaAppRepository = EmpresaRepository(conexionAgendaza.session)
geserveAppQueries = Repositorio(conexionGeserveApp.session)  # Util cuando usamos nativeQuery
agendazaAppQueries = Repositorio(conexionAgendaza.session)  # Util cuando usamos nativeQuery
capacidadRepository = CapacidadRepository(conexionAgendaza.session)

cargoRepository = CargoRepository(conexionAgendaza.session)
salonLegacyRepository = SalonLegacyRepositorio(conexionGeserveApp.session)
nativeQuerys = NativeQuerys()
foreignLegacyVsNewAux = ForeignLegacyVsNewAux()
extraRepository = ExtraRepository(conexionAgendaza.session)
precioConFechaExtraVariableCateringRepository = PrecioConFechaExtraVariableCateringRepository(
    conexionGeserveApp.session)
precioConFechaExtraSubTipoEventoRepository = PrecioConFechaExtraSubTipoEventoRepository(conexionGeserveApp.session)
precioConFechaExtraTipoCateringRepository = PrecioConFechaExtraTipoCateringRepository(conexionGeserveApp.session)
precioConFechaExtraVariableEventoRepository = PrecioConFechaExtraVariableEventoRepository(conexionGeserveApp.session)
precioConFechaExtraRepository = PrecioConFechaExtraRepository(conexionAgendaza.session)
capacidadUtil = CapacidadUtil()
tipoEventoRepository = TipoEventoRepository(conexionAgendaza.session)
precioConFechaEventoRepository = PrecioConFechaEventoRepository(conexionAgendaza.session)
eventoRepository = EventoRepository(conexionAgendaza.session)
pagoRepository = PagoRepository(conexionAgendaza.session)
servicioRepository = ServicioRepository(conexionAgendaza.session)
tipoEventoServicioRepository = TipoEventoServicioRepository(conexionAgendaza.session)
eventoExtraVariableRepository = EventoExtraVariableRepository(conexionAgendaza.session)
eventoExtraRepository = EventoExtraRepository(conexionAgendaza.session)
tipoEventoExtraRepository = TipoEventoExtraRepository(conexionAgendaza.session)
empresaServicioRepository = EmpresaServicioRepository(conexionAgendaza.session)
logging.basicConfig(level=logging.INFO)
infoLog = InfoLog()
# Ejecutar el bucle principal
asyncio.run(main())
