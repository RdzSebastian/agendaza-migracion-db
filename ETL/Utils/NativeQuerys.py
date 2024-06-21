class NativeQuerys:
    queryVARIABLE_CATERING = """select distinct etc.id as id ,etc.nombre as nombre , 'VARIABLE_CATERING' as tipoExtra , extra.salon_id as empresa_id 
    	from extra_variable_catering etc 
    	join precio_con_fecha_extra_variable_catering extra 
    	on etc.id = extra_variable_catering_id;"""

    queryEvento = """ 
        select distinct este.id as id,este.nombre as nombre  , extra.salon_id as empresa_id from extra_sub_tipo_evento este 
    	join precio_con_fecha_extra_sub_tipo_evento extra  on este.id = extra.extra_sub_tipo_evento_id ;
        """

    queryTipoCatering = """
        select distinct este.id as id ,este.nombre as nombre  , extra.salon_id as empresa_id
    	from tipo_catering este 
    	join precio_con_fecha_tipo_catering extra  on este.id = extra.tipo_catering_id ; 
        """

    queryVariable_Evento = """  	
        select distinct este.id as id ,este.nombre  as nombre , extra.salon_id as empresa_id
    	from extra_variable_sub_tipo_evento este 
    	join precio_con_fecha_extra_variable_sub_tipo_evento extra  on este.id = extra.extra_variable_sub_tipo_evento_id; 
        """

    queryForCargoETL = query = """
    SELECT u.id_Agendaza AS usuario_id, r.id, r.nombre AS tipo_cargo, s.id AS empresa_id
    FROM usuario u
    JOIN rol r ON u.rol_id = r.id
    JOIN evento e ON u.id = e.usuario_id
    JOIN salon s ON s.id = e.salon_id
    GROUP BY u.id, r.id, s.id
    ORDER BY usuario_id;
    """

    queryForCapacidadGeserveApp = """select distinct capacidad_adultos , capacidad_ninos  from capacidad;"""

    queryForCapacidadGeserveAppFullPostMigration = """ SELECT  * FROM  capacidad;"""

    querySubTipoEventoLegacy = """
            SELECT DISTINCT
            STE.ID,
            STE.NOMBRE,
            STE.DURACION AS CANTIDAD_DURACION,
            STE.CAPACIDAD_ID,
            UPPER(TE.NOMBRE) AS DURACION,
            PCFS.SALON_ID AS EMPRESA_ID
            
        FROM
            SUB_TIPO_EVENTO STE
            JOIN TIPO_EVENTO TE ON TE.ID = STE.TIPO_EVENTO_ID
            JOIN PRECIO_CON_FECHA_SUB_TIPO_EVENTO PCFS ON  STE.ID =PCFS.SUB_TIPO_EVENTO_ID
    """

    queryForPrecioConFechaSubTipoEventoGeserveApp = """
            SELECT
            ID,
            PRECIO,
            DESDE,
            HASTA,
            SALON_ID AS EMPRESA_ID,
            SUB_TIPO_EVENTO_ID AS TIPO_EVENTO_ID
        FROM
            PRECIO_CON_FECHA_SUB_TIPO_EVENTO
        WHERE PRECIO > 0
            ;
    """

    queryForEvento = """
    SELECT
        E.ID,
        CA.CATERING_OTRO AS CATERING_OTRO,
        E.CODIGO AS CODIGO,
        E.DESCUENTO,
        E.EXTRA_OTRO,
        E.ENDD AS FIN ,
        E.STARTD AS INICIO,
        E.NOMBRE ,
        E.CAPACIDAD_ID,
        E.CLIENTE_ID,
        E.SALON_ID AS EMPRESA_ID ,
        E.USUARIO_ID AS ENCARGADO_ID,
        E.SUB_TIPO_EVENTO_ID AS TIPO_EVENTO_ID
    FROM
        EVENTO E
        JOIN CATERING CA ON E.CATERING_ID = CA.ID
    ORDER BY
        E.ID ASC
        ;
    """

    queryForPago = """
    SELECT
        P.ID,
        P.FECHA AS FECHA ,
        P.PAGO AS MONTO,
        UPPER(MDP.NOMBRE) AS MEDIO_DE_PAGO,
        P.USUARIO_ID AS ENCARGADO_ID,
        P.EVENTO_ID AS EVENTO_ID
        
    FROM
        PAGO P
        JOIN MEDIO_DE_PAGO MDP ON P.MEDIO_DE_PAGO_ID = MDP.ID;
    """


    queryForServicio = """
    SELECT
        DISTINCT 
        S.ID,
        S.NOMBRE ,
        PCF.SALON_ID AS EMPRESA_ID
        
    FROM SERVICIO S
        JOIN SUB_TIPO_EVENTO_SERVICIO STES ON S.ID = STES.SERVICIO_ID
        JOIN SUB_TIPO_EVENTO STE ON STE.ID = STES.SUB_TIPO_EVENTO_ID
        JOIN PRECIO_CON_FECHA_SUB_TIPO_EVENTO PCF ON PCF.SUB_TIPO_EVENTO_ID = STE.ID
    ORDER BY S.ID ASC
;"""
