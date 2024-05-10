from ETL.Conexión import conexionAgendaza
from ETL.Conexión import conexionGeserveApp
import pandas as pd

from ETL.gerservapp_legacy.Legacy import Legacy
import traceback

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

    visualizar(usuarioAgendazaList)

    # LOAD/CARGA/MIGRACION -> ETL Finalizado
    usuarioAgendazaRepository.saveAll(usuarioAgendazaList)


async def ETLEmpresa():
    global empresaGeserveAppRepository
    global empresaAgendazaAppRepository
    query = """
    select Distinct s.id as salon_id , s.calle as calle , u.mail as email , s.municipio , s.nombre, s.numero 
    from usuario u
    join evento e on u.id = e.usuario_id
    join salon s on s.id = e.salon_id 
    where u.mail = 'miixeventos1@gmail.com';
    """

    resultado = empresaGeserveAppRepository.sqlNativeQuery(query)
    empresas = []

    for row in resultado:
        empresa = Empresa(
            nombre=row.nombre,
            telefono=1111111111,  # Establecer el teléfono adecuadamente
            email=row.email,
            calle=row.calle,
            numero=row.numero,
            municipio=row.municipio,
            id_legacy=row.salon_id,
            dtype='Salon'

        )
        empresas.append(empresa)

    empresaAgendazaAppRepository.saveAll(empresas)


#################################################################################################################
'''
A partir de aquí  comienza el script de migración 
'''


##############################################################################################################
async def main():
    global clienteReserveappRepository
    global usuarioLegacyRepository
    global usuarioAgendazaRepository

    await columnasAuxiliares()
    await ETLUsuario()
    await ETLCliente()
    await ETLEmpresa()

    conexionAgendaza.cerrar_conexion()
    conexionGeserveApp.cerrar_conexion()


conexionAgendaza.realizar_conexion()
conexionGeserveApp.realizar_conexion()

from repositorio.Repository import UsuarioLegacyRepository
from repositorio.UsuarioRepository import UsuarioRepository
from repositorio.ClienteRepository import ClienteLegacyRepository
from repositorio.EmpresaRepository import EmpresaRepository
from ETL.agendaza.Empresa import Empresa

usuarioLegacyRepository = UsuarioLegacyRepository(conexionGeserveApp.session)
usuarioAgendazaRepository = UsuarioRepository(conexionAgendaza.session)
clienteReserveappRepository = ClienteLegacyRepository(conexionGeserveApp.session)
empresaGeserveAppRepository = EmpresaRepository(conexionGeserveApp.session)
empresaAgendazaAppRepository = EmpresaRepository(conexionAgendaza.session)
# Ejecutar el bucle principal
asyncio.run(main())
