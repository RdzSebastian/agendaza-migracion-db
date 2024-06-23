class NativeQuerys:
    queryVARIABLE_CATERING = """
    SELECT
        DISTINCT EXTRA.ID , EXTRA.NOMBRE , E.SALON_ID AS EMPRESA_ID
    FROM
        EXTRA_VARIABLE_CATERING EXTRA
        JOIN CATERING_EXTRA_VARIABLE_CATERING CEXTRA ON EXTRA.ID = CEXTRA.EXTRA_VARIABLE_CATERING_ID
        JOIN CATERING CA ON CA.ID =  CEXTRA.CATERING_ID
        JOIN EVENTO E ON E.CATERING_ID = CA.ID
	WHERE E.SALON_ID IS NOT NULL
    
	UNION
        
    SELECT DISTINCT
        ETC.ID AS ID,
        ETC.NOMBRE AS NOMBRE,
        EXTRA.SALON_ID AS EMPRESA_ID
    FROM
        EXTRA_VARIABLE_CATERING ETC
        JOIN PRECIO_CON_FECHA_EXTRA_VARIABLE_CATERING EXTRA ON ETC.ID = EXTRA_VARIABLE_CATERING_ID
    ORDER BY ID ASC
	;
    """

    querySubTipoEvento = """ 
        SELECT DISTINCT
            EXTRA.ID,
            EXTRA.NOMBRE,
            E.SALON_ID AS EMPRESA_ID
        FROM
            EXTRA_SUB_TIPO_EVENTO EXTRA
            JOIN EVENTO_EXTRA_SUB_TIPO_EVENTO NM ON EXTRA.ID = NM.EXTRA_SUB_TIPO_EVENTO_ID
            JOIN EVENTO E ON E.ID = NM.EVENTO_ID
		WHERE E.SALON_ID IS NOT NULL
        
        UNION 
        
        SELECT DISTINCT
            ESTE.ID AS ID,
            ESTE.NOMBRE AS NOMBRE,
            EXTRA.SALON_ID AS EMPRESA_ID
        FROM
            EXTRA_SUB_TIPO_EVENTO ESTE
            JOIN PRECIO_CON_FECHA_EXTRA_SUB_TIPO_EVENTO EXTRA ON ESTE.ID = EXTRA.EXTRA_SUB_TIPO_EVENTO_ID
        
        ORDER BY
            ID ASC;

        """

    queryTipoCatering = """
        SELECT DISTINCT
            ESTE.ID AS ID,
            ESTE.NOMBRE AS NOMBRE,
            EXTRA.SALON_ID AS EMPRESA_ID
        FROM
            TIPO_CATERING ESTE
            JOIN PRECIO_CON_FECHA_TIPO_CATERING EXTRA ON ESTE.ID = EXTRA.TIPO_CATERING_ID
        
        UNION
        
        SELECT
            DISTINCT EXTRA.ID AS ID,
            EXTRA.NOMBRE,
            E.SALON_ID AS EMPRESA_ID
        FROM
            TIPO_CATERING EXTRA
            JOIN CATERING_TIPO_CATERING NM ON EXTRA.ID = NM.TIPO_CATERING_ID
            JOIN CATERING CA ON NM.CATERING_ID = CA.ID
            JOIN EVENTO E ON E.CATERING_ID = CA.ID
            WHERE E.SALON_ID IS NOT NULL
        ORDER BY ID ASC
            ;
        """

    queryVariable_Evento = """  	
       SELECT DISTINCT
            ESTE.ID AS ID,
            ESTE.NOMBRE AS NOMBRE,
            EXTRA.SALON_ID AS EMPRESA_ID
        FROM
            EXTRA_VARIABLE_SUB_TIPO_EVENTO ESTE
            JOIN PRECIO_CON_FECHA_EXTRA_VARIABLE_SUB_TIPO_EVENTO EXTRA ON ESTE.ID = EXTRA.EXTRA_VARIABLE_SUB_TIPO_EVENTO_ID
        
        UNION
        
        SELECT DISTINCT 
            EXTRA.ID AS ID,
            EXTRA.NOMBRE AS NOMBRE,
            E.SALON_ID AS EMPRESA_ID
        FROM
            EXTRA_VARIABLE_SUB_TIPO_EVENTO EXTRA
            JOIN EVENTO_EXTRA_VARIABLE_SUB_TIPO_EVENTO EEXTRA ON EEXTRA.EXTRA_VARIABLE_SUB_TIPO_EVENTO_ID =EXTRA.ID
            JOIN EVENTO E ON E.ID = EEXTRA.EVENTO_ID
            WHERE E.SALON_ID IS NOT NULL
        ORDER BY ID ASC;
        """


    queryForExtrasMigradosNoDuplicadosAgendaza = """
    SELECT
        NOMBRE,
        TIPO_EXTRA,
        EMPRESA_ID,
        EXTRA_VARIABLE_CATERING_ID_LEGACY,
        EXTRA_SUB_TIPO_EVENTO_ID_LEGACY,
        TIPO_CATERING_ID_LEGACY,
        EXTRA_VARIABLE_SUB_TIPO_EVENTO_ID_LEGACY
    FROM
        EXTRA
    WHERE
        NOMBRE IN (
            SELECT
                NOMBRE
            FROM
                EXTRA
            WHERE
                EXTRA_VARIABLE_CATERING_ID_LEGACY IS NOT NULL
                OR EXTRA_SUB_TIPO_EVENTO_ID_LEGACY IS NOT NULL
                OR TIPO_CATERING_ID_LEGACY IS NOT NULL
                OR EXTRA_VARIABLE_SUB_TIPO_EVENTO_ID_LEGACY IS NOT NULL
            GROUP BY
                NOMBRE,
                TIPO_EXTRA
            HAVING
                COUNT(*) = 1
	)


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

    queryForSubTipoEventoServicio = """
    SELECT
        SUB_TIPO_EVENTO_ID AS TIPO_EVENTO_ID,
        SERVICIO_ID
    FROM
	    SUB_TIPO_EVENTO_SERVICIO;
    
    """

    queryForEventoExtraVariable = """
    SELECT
        ID,
        CANTIDAD,
        EVENTO_ID,
        EXTRA_VARIABLE_SUB_TIPO_EVENTO_ID AS EXTRA_ID
    FROM
        EVENTO_EXTRA_VARIABLE_SUB_TIPO_EVENTO;
    """

    queryForEventoExtraSubTipoEvento = """
    SELECT
        EVENTO_ID,
        EXTRA_SUB_TIPO_EVENTO_ID AS EXTRA_ID
    FROM
        EVENTO_EXTRA_SUB_TIPO_EVENTO
    """

    queryForSubTipoEventoTipoCatering= """
    SELECT
        SUB_TIPO_EVENTO_ID AS TIPO_EVENTO_ID,
        TIPO_CATERING_ID AS EXTRA_ID
    FROM
        SUB_TIPO_EVENTO_TIPO_CATERING;
    """

    queryFroSubTipoEvento ="""
    SELECT
        SUB_TIPO_EVENTO_ID AS TIPO_EVENTO_ID,
        EXTRA_ID AS EXTRA_ID
    FROM
        SUB_TIPO_EVENTO_EXTRA;
    """

    queryForSubTipoEventoExtraVariableCatering = """
    SELECT
        SUB_TIPO_EVENTO_ID AS TIPO_EVENTO_ID,
        EXTRA_VARIABLE_CATERING_ID AS EXTRA_ID
    FROM
        SUB_TIPO_EVENTO_EXTRA_VARIABLE_CATERING;  
    """

    queryForSubTipoEventoExtraVariable = """
    SELECT
        SUB_TIPO_EVENTO_ID AS TIPO_EVENTO_ID,
        EXTRA_VARIABLE_ID AS EXTRA_ID
    FROM
        SUB_TIPO_EVENTO_EXTRA_VARIABLE;
    
    """

