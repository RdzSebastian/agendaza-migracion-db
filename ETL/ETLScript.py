from ETL.Conexión import conexionAgendaza
from ETL.Conexión import conexionGeserveApp

conexionAgendaza.realizar_conexion()
conexionGeserveApp.realizar_conexion()




##Obligatorio que las importaciones venga despues de realizar la conexion. Mas adelante ver si se puede solucionar
##pero no es prioridad

from ETL.gerservapp_legacy.UsuarioLegacy import UsuarioLegacy
from repositorio.Repository import UsuarioLegacyRepository


user1 = UsuarioLegacy(nombre='Mauricio',
                      apellido='Martinez',
                      username='TheMauricio',
                      password='adasfasfasf',
                      mail='mauricio@mail.com',
                      account_non_expired=False,
                      account_non_locked=True,
                      credentials_non_expired=True,
                      enabled=True)

usuarioLegacyRepository = UsuarioLegacyRepository(conexionGeserveApp.Session)

usuarioLegacyRepository.save(user1)