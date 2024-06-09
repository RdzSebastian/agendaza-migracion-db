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
