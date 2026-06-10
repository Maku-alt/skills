import re

def generate_debugerror_procedure(nombre_corto_proyecto, query, tipo_proyecto, parametro_fecha, ambiente='prod'):
    """
    Parámetros:
    - nombre_corto_proyecto (str): Nombre corto del proyecto.
      Ejemplo: si el proyecto es "acom-b2c-movil-portinwinback-2024", el nombre corto sería "portinwinback", puedes distinguirlo con el año.
    - query (str): Sentencia SQL validada que se desea convertir en procedimiento almacenado.
    - tipo_proyecto (str): Tipo de proyecto que afecta la nomenclatura del procedimiento.
      posibles valores = ["mod|ana|proc|con"]
      Recordar Nomenclaturas de SAM = "sp|debug|error"_["mod|ana|proc|con"]_["dev|prod|tmp"]_[nombre_proyecto]_["target|fuente|poblacion|dataset|output"]_["hist"]
    - parametro_fecha (str): Nombre del parámetro de fecha que se utilizará en el procedimiento almacenado.
    
    Retorna:
    - str: Script SQL con la estructura del procedimiento almacenado, incluyendo la gestión de errores y logs.
    
    Descripción:
    1. Se crean nombres de las tablas de debug y error basados en el nombre del proyecto.
    2. Se genera un procedimiento almacenado que ejecutará la query proporcionada y manejará errores.
    3. Se agregan llamadas a un procedimiento de logging `sp_debugerror` antes y después de la ejecución de la query.
    4. Se aseguran estructuras de logs para almacenar mensajes de depuración y errores.

    """
    tabla_debug = f'debug_{tipo_proyecto}_{ambiente}_{nombre_corto_proyecto}_hist'
    tabla_error = f'error_{tipo_proyecto}_{ambiente}_{nombre_corto_proyecto}_hist'
    sp_debugerror = f'sp_{tipo_proyecto}_{ambiente}_debug_{nombre_corto_proyecto}'


    sp_proyecto = f'sp_{tipo_proyecto}_{ambiente}_{nombre_corto_proyecto}'

    procedure_name = ":procedure_name"
    parametro_fecha_sp = 'p_' + parametro_fecha

    
    query_lines = []
    lines = query.split('\\n')
    call_count = 1

    for line in lines:
        # Buscar la palabra TABLE seguida del nombre de tabla
        match = re.search(r'\\bTABLE\\s+([^\\s(]+)', line, re.IGNORECASE)
        if match:
            table_name = match.group(1)
            query_lines.append(f"CALL dbi_min.{sp_debugerror}(:{parametro_fecha_sp}, {procedure_name}, '{table_name}', '', {call_count});")
            call_count += 1
        query_lines.append(line)

    query_v2 = "\\n".join(query_lines)
    call_count_f = call_count

    
    drop_table_calls = '\\n'.join([
        line for line in query_v2.split('\\n') 
        if any(line.strip().lower().startswith(prefix.lower()) for prefix in ('CALL SP_SAM_DROPTABLE', 'CALL DBI_MIN.SP_SAM_DROPTABLE'))
    ])

    
    procedure_template = f"""
    
--#==========================================================================================================#--
CALL SP_SAM_DROPTABLE('dbi_min.error_{tipo_proyecto}_prod_{nombre_corto_proyecto}_hist');
CREATE TABLE dbi_min.error_{tipo_proyecto}_prod_{nombre_corto_proyecto}_hist (
    {parametro_fecha}    VARCHAR(20),
    sp_name         VARCHAR(50),
    mensaje_error   VARCHAR(500),
    execution_date  DATE,
    execution_time  TIME
) PRIMARY INDEX({parametro_fecha}, sp_name, execution_date, execution_time);

CALL SP_SAM_DROPTABLE('dbi_min.debug_{tipo_proyecto}_prod_{nombre_corto_proyecto}_hist');
CREATE TABLE dbi_min.debug_{tipo_proyecto}_prod_{nombre_corto_proyecto}_hist (
    {parametro_fecha}   VARCHAR(20),
    sp_name        VARCHAR(150),
    user_name      VARCHAR(20),
    execution_date DATE,
    execution_time TIME,
    table_name     VARCHAR(150),
    message        VARCHAR(255),
    execution_order          INT
) PRIMARY INDEX({parametro_fecha}, sp_name, execution_date, execution_time,execution_order);

-- Creación del procedimiento de logging.
CREATE PROCEDURE dbi_min.sp_{tipo_proyecto}_prod_debug_{nombre_corto_proyecto}(
    IN {parametro_fecha} VARCHAR(20),
    IN sp_name VARCHAR(150),
    IN table_name VARCHAR(150),
    IN text VARCHAR(255),
    IN execution_order INT
)
BEGIN
    INSERT INTO dbi_min.debug_{tipo_proyecto}_prod_{nombre_corto_proyecto}_hist 
    VALUES (:{parametro_fecha}, :sp_name, USER, CURRENT_DATE, CURRENT_TIME, :table_name, :text, :execution_order);
END;
--#==========================================================================================================#--
    
REPLACE PROCEDURE dbi_min.{sp_proyecto}(
   IN {parametro_fecha_sp} DATE 
)
BEGIN

DECLARE procedure_name VARCHAR(75);
DECLARE mensaje_error VARCHAR(500);

DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        GET DIAGNOSTICS EXCEPTION 1 mensaje_error = MESSAGE_TEXT;
        INSERT INTO {tabla_error} VALUES (:{parametro_fecha_sp}, :procedure_name, :mensaje_error, CURRENT_DATE, CURRENT_TIME);
    END;

SET procedure_name = '{sp_proyecto}';

CALL dbi_min.{sp_debugerror}(:{parametro_fecha_sp}, :procedure_name, 'Inicio del proceso', 'INICIO', 0);

{query_v2}

{drop_table_calls}

CALL dbi_min.{sp_debugerror}(:{parametro_fecha_sp}, :procedure_name, 'Fin del proceso', 'FIN', {call_count_f});

END;
    """
    return procedure_template.strip()


def generate_debugerror_procedure_moba2025(nombre_corto_proyecto, query, tipo_proyecto, parametro_fecha, ambiente='prod'):
    """
    Parámetros:
    - nombre_corto_proyecto (str): Nombre corto del proyecto.
      Ejemplo: si el proyecto es "acom-b2c-movil-portinwinback-2024", el nombre corto sería "portinwinback", puedes distinguirlo con el año.
    - query (str): Sentencia SQL validada que se desea convertir en procedimiento almacenado.
    - tipo_proyecto (str): Tipo de proyecto que afecta la nomenclatura del procedimiento.
      posibles valores = ["mod|ana|proc|con"]
      Recordar Nomenclaturas de SAM = "sp|debug|error"_["mod|ana|proc|con"]_["dev|prod|tmp"]_[nombre_proyecto]_["target|fuente|poblacion|dataset|output"]_["hist"]
    - parametro_fecha (str): Nombre del parámetro de fecha que se utilizará en el procedimiento almacenado.
    
    Retorna:
    - str: Script SQL con la estructura del procedimiento almacenado, incluyendo la gestión de errores y logs.
    
    Descripción:
    1. Se crean nombres de las tablas de debug y error basados en el nombre del proyecto.
    2. Se genera un procedimiento almacenado que ejecutará la query proporcionada y manejará errores.
    3. Se agregan llamadas a un procedimiento de logging `sp_debugerror` antes y después de la ejecución de la query.
    4. Se aseguran estructuras de logs para almacenar mensajes de depuración y errores.

    """
    tabla_debug = f'debug_{tipo_proyecto}_{ambiente}_{nombre_corto_proyecto}_moba2025_hist'
    tabla_error = f'error_{tipo_proyecto}_{ambiente}_{nombre_corto_proyecto}_moba2025_hist'
    sp_debugerror = f'sp_{tipo_proyecto}_{ambiente}_debug_{nombre_corto_proyecto}_moba2025'


    sp_proyecto = f'sp_{tipo_proyecto}_{ambiente}_{nombre_corto_proyecto}_MOBA2025'

    procedure_name = ":procedure_name"
    parametro_fecha_sp = 'p_' + parametro_fecha

    lines = query.split('\n')

    user_declares = []
    user_sets = []
    body_lines = []

    # Parse query to separate components
    for line in lines:
        clean = line.strip().lower()
        if clean.startswith('declare '):
            user_declares.append(line)
        elif clean.startswith('set '):
            user_sets.append(line)
        else:
            if clean: # Skip empty lines in body initially
                 body_lines.append(line)
            elif body_lines: # Keep empty lines only if body has started
                 body_lines.append(line)

    query_lines = []
    call_count = 1

    for line in body_lines:
        # Buscar la palabra TABLE seguida del nombre de tabla
        match = re.search(r'\bTABLE\s+([^\s(]+)', line, re.IGNORECASE)
        if match:
            table_name = match.group(1)
            query_lines.append(f"CALL dbi_min.{sp_debugerror}(:{parametro_fecha_sp}, {procedure_name}, '{table_name}', '', {call_count});")
            call_count += 1
        
        # Enforce dbi_min. prefix for SP_SAM_DROPTABLE in body
        if 'call sp_sam_droptable' in line.lower() and 'dbi_min.' not in line.lower():
            line = re.sub(r'call\s+sp_sam_droptable', 'CALL dbi_min.SP_SAM_DROPTABLE', line, flags=re.IGNORECASE)
            
        query_lines.append(line)

    query_v2 = "\n".join(query_lines)
    call_count_f = call_count

    # Extract declares and sets text
    user_declares_text = "\n".join(user_declares)
    user_sets_text = "\n".join(user_sets)
    
    drop_lines = []
    for line in query_v2.split('\n'):
        clean = line.strip().lower()
        if clean.startswith('call sp_sam_droptable'):
            # Enforce dbi_min. prefix
            drop_lines.append(re.sub(r'call\s+sp_sam_droptable', 'CALL dbi_min.SP_SAM_DROPTABLE', line, flags=re.IGNORECASE))
        elif clean.startswith('call dbi_min.sp_sam_droptable'):
            drop_lines.append(line)
    
    drop_table_calls = '\n'.join(drop_lines)

    
    procedure_template = f"""

--#==========================================================================================================#--
CALL SP_SAM_DROPTABLE('dbi_min.{tabla_error}');
CREATE TABLE dbi_min.{tabla_error} (
    {parametro_fecha}    VARCHAR(20),
    sp_name         VARCHAR(50),
    mensaje_error   VARCHAR(500),
    execution_date  DATE,
    execution_time  TIME
) PRIMARY INDEX({parametro_fecha}, sp_name, execution_date, execution_time);

CALL SP_SAM_DROPTABLE('dbi_min.{tabla_debug}');
CREATE TABLE dbi_min.{tabla_debug} (
    {parametro_fecha}   VARCHAR(20),
    sp_name        VARCHAR(150),
    user_name      VARCHAR(20),
    execution_date DATE,
    execution_time TIME,
    table_name     VARCHAR(150),
    message        VARCHAR(255),
    execution_order          INT
) PRIMARY INDEX({parametro_fecha}, sp_name, execution_date, execution_time,execution_order);

-- Creación del procedimiento de logging.
CREATE PROCEDURE dbi_min.{sp_debugerror}(
    IN {parametro_fecha} VARCHAR(20),
    IN sp_name VARCHAR(150),
    IN table_name VARCHAR(150),
    IN text VARCHAR(255),
    IN execution_order INT
)
BEGIN
    INSERT INTO dbi_min.{tabla_debug} 
    VALUES (:{parametro_fecha}, :sp_name, USER, CURRENT_DATE, CURRENT_TIME, :table_name, :text, :execution_order);
END;
--#==========================================================================================================#--
    
REPLACE PROCEDURE dbi_min.{sp_proyecto}(
   IN {parametro_fecha_sp} DATE 
)
BEGIN

DECLARE procedure_name VARCHAR(75);
DECLARE mensaje_error VARCHAR(500);
{user_declares_text}

DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        GET DIAGNOSTICS EXCEPTION 1 mensaje_error = MESSAGE_TEXT;
        INSERT INTO {tabla_error} VALUES (:{parametro_fecha_sp}, :procedure_name, :mensaje_error, CURRENT_DATE, CURRENT_TIME);
    END;

SET procedure_name = '{sp_proyecto}';
{user_sets_text}

CALL dbi_min.{sp_debugerror}(:{parametro_fecha_sp}, :procedure_name, 'Inicio del proceso', 'INICIO', 0);

{query_v2}

{drop_table_calls}

CALL dbi_min.{sp_debugerror}(:{parametro_fecha_sp}, :procedure_name, 'Fin del proceso', 'FIN', {call_count_f});

END;
    """
    return procedure_template.strip()
