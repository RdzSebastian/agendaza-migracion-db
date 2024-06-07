from ETL.Conexión import conexionAgendaza
from ETL.Conexión import conexionGeserveApp
import pandas as pd
from typing import List

from ETL.Utils.ForeignLegacyVsNewAux import ForeignLegacyVsNewAux
from ETL.Utils.NativeQuerys import NativeQuerys
from ETL.gerservapp_legacy.Legacy import Legacy
import traceback
import copy

import asyncio


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

    usuarioAgendazaRepository.sqlNativeQuery("ALTER TABLE usuario ADD COLUMN id_usuario_legacy INTEGER unique ")
    usuarioAgendazaRepository.sqlNativeQuery("ALTER TABLE usuario ADD COLUMN id_cliente_legacy INTEGER unique ")
    usuarioLegacyRepository.sqlNativeQuery("ALTER TABLE usuario ADD COLUMN id_agendaza INTEGER unique")
    empresaAgendazaAppRepository.sqlNativeQuery("ALTER TABLE empresa ADD COLUMN id_legacy INTEGER unique")
    cargoRepository.sqlNativeQuery("ALTER TABLE cargo ADD COLUMN es_legacy BOOLEAN")
    geserveAppQueries.sqlNativeQuery("ALTER TABLE salon ADD COLUMN id_agendaza INTEGER unique")
    agendazaAppQueries.sqlNativeQuery("ALTER TABLE extra ADD COLUMN extra_variable_catering_id_legacy INTEGER")
    agendazaAppQueries.sqlNativeQuery("ALTER TABLE extra ADD COLUMN EXTRA_SUB_TIPO_EVENTO_ID_LEGACY INTEGER")
    agendazaAppQueries.sqlNativeQuery("ALTER TABLE extra ADD COLUMN tipo_catering_id_legacy INTEGER")
    agendazaAppQueries.sqlNativeQuery("ALTER TABLE extra ADD COLUMN extra_variable_sub_tipo_evento_id_legacy INTEGER")


#

async def ETLUsuario():
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


async def ETLCliente():
    global clienteReserveappRepository
    global usuarioAgendazaRepository

    # Extraccion
    clienteLegacyList = clienteReserveappRepository.getAll()
    # TRANSFORMACION
    usuarioAgendazaList = transformacion(clienteLegacyList)

    # LOAD/CARGA/MIGRACION -> ETL Finalizado
    usuarioAgendazaRepository.saveAll(usuarioAgendazaList)


async def ETLEmpresa():
    global salonLegacyRepository
    global empresaAgendazaAppRepository
    salones = salonLegacyRepository.getAll()
    listaEmpresa = transformacion(salones)

    empresaAgendazaAppRepository.saveAll(listaEmpresa)

    for item in salones:
        item.asignarIdAgendaza()

    salonLegacyRepository.saveAll(salones)

    return listaEmpresa


async def cargoETL(empresalist):
    global geserveAppQueries
    global cargoRepository
    list = empresalist
    global nativeQuerys

    resultado = geserveAppQueries.sqlNativeQuery(nativeQuerys.queryForCargoETL)
    cargos = []

    for row in resultado:
        cargo = Cargo(
            usuario_id=row.usuario_id,
            tipo_cargo=row.tipo_cargo
        )

        cargo.setEmpresaId(list, row.empresa_id)
        cargos.append(cargo)

    cargoRepository.saveAll(cargos)


async def extraETL(empresalist, extraLegacyRepository):
    global extraRepository

    extraLegacyList = extraLegacyRepository.getAll()

    extraList = transformacion(extraLegacyList)

    finalList = []

    empresaMigradaIdList = [item.id for item in empresalist]

    for idItem in empresaMigradaIdList:
        for extraItem in extraList:
            extraItemCopy = copy.deepcopy(extraItem)
            extraItemCopy.empresa_id = idItem
            finalList.append(extraItemCopy)

    extraRepository.saveAll(finalList)

    await precioConFechaExtraETL(extraLegacyList, empresalist)


async def precioConFechaExtraETL(extraLegacyList, empresalist):
    precioConFechaList = []
    empresa_id_id_legacy = {}
    for item in empresalist:
        empresa_id_id_legacy[item.id] = item.id_legacy

    for extraLegacy in extraLegacyList:
        for precio in extraLegacy.listaPrecioFechas():
            precioConFechaList.append(precio)

    visualizar(precioConFechaList)


async def precioConFechaExtraETL2(query, foreignLegacyVsNewAux, tipo):
    global extraRepository
    extraList = geserveAppQueries.sqlNativeQuery(query)
    empresa_id_id_legacy = foreignLegacyVsNewAux.empresa_id_legacy_vs_agendaza_id
    extraReturn = []

    for row in extraList:
        extra = Extra(nombre=row.nombre, tipo_extra=tipo)
        extra.empresa_id = empresa_id_id_legacy.get(row.empresa_id)
        await definirQueIdSetear(extra, row.id)
        extraReturn.append(extra)

    extraRepository.saveAll(extraReturn)


async def definirQueIdSetear(extra, id):
    if extra.tipo_extra == "VARIABLE_CATERING":
        extra.extra_variable_catering_id_legacy = id

    if extra.tipo_extra == "EVENTO":
        extra.extra_sub_tipo_evento_id_legacy = id

    if extra.tipo_extra == "TIPO_CATERING":
        extra.tipo_catering_id_legacy = id

    if extra.tipo_extra == "VARIABLE_EVENTO":
        extra.extra_variable_sub_tipo_evento_id_legacy = id


#################################################################################################################


##############################################################################################################
async def main():
    global clienteReserveappRepository
    global usuarioLegacyRepository
    global usuarioAgendazaRepository
    global nativeQuerys
    global foreignLegacyVsNewAux

    await columnasAuxiliares()
    await ETLUsuario()
    await ETLCliente()
    listaEmpresa = await ETLEmpresa()
    await cargoETL(listaEmpresa)
    foreignLegacyVsNewAux.setEmpresaIds(listaEmpresa)

    # await extraETL(empresa, extraSubTipoEventoLegacyRepository)
    # await extraETL(empresa, extraVariableCateringLegacyRepository)
    # await extraETL(empresa, extraTipoCateringLegacy)
    # await extraETL(empresa, extraVariableSubTipoEventoRepository)

    await precioConFechaExtraETL2(nativeQuerys.queryVARIABLE_CATERING, foreignLegacyVsNewAux, "VARIABLE_CATERING")
    await precioConFechaExtraETL2(nativeQuerys.queryEvento, foreignLegacyVsNewAux, "EVENTO")
    await precioConFechaExtraETL2(nativeQuerys.queryTipoCatering, foreignLegacyVsNewAux, "TIPO_CATERING")
    await precioConFechaExtraETL2(nativeQuerys.queryVariable_Evento, foreignLegacyVsNewAux, "VARIABLE_EVENTO")

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
from repositorio.ExtraRepository import ExtraVariableCateringLegacyRepository, ExtraRepository, \
    ExtraSubTipoEventoLegacyRepository, ExtraSubTipoCateringLegacyRepository, ExtraVariableSubTipoEventoRepository
from ETL.agendaza.Extra import Extra

usuarioLegacyRepository = UsuarioLegacyRepository(conexionGeserveApp.session)
usuarioAgendazaRepository = UsuarioRepository(conexionAgendaza.session)
clienteReserveappRepository = ClienteLegacyRepository(conexionGeserveApp.session)
empresaGeserveAppRepository = EmpresaRepository(conexionGeserveApp.session)
empresaAgendazaAppRepository = EmpresaRepository(conexionAgendaza.session)
geserveAppQueries = Repositorio(conexionGeserveApp.session)  # Util cuando usamos nativeQuery
agendazaAppQueries = Repositorio(conexionAgendaza.session)  # Util cuando usamos nativeQuery

cargoRepository = CargoRepository(conexionAgendaza.session)
salonLegacyRepository = SalonLegacyRepositorio(conexionGeserveApp.session)
extraVariableCateringLegacyRepository = ExtraVariableCateringLegacyRepository(conexionGeserveApp.session)
extraSubTipoEventoLegacyRepository = ExtraSubTipoEventoLegacyRepository(conexionGeserveApp.session)
extraTipoCateringLegacy = ExtraSubTipoCateringLegacyRepository(conexionGeserveApp.session)
extraVariableSubTipoEventoRepository = ExtraVariableSubTipoEventoRepository(conexionGeserveApp.session)
nativeQuerys = NativeQuerys()
foreignLegacyVsNewAux = ForeignLegacyVsNewAux()
extraRepository = ExtraRepository(conexionAgendaza.session)
# Ejecutar el bucle principal
asyncio.run(main())
