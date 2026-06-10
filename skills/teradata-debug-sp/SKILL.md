---
name: teradata-debug-sp
description: "Genera Store Procedures de Teradata con infraestructura de debug y manejo de errores. Usar cuando el agente necesite transformar queries SQL en procedimientos almacenados de producción con: (1) Tablas de debug y error, (2) Logging automático antes de cada CREATE TABLE, (3) Manejo de excepciones SQL, (4) Nomenclatura estándar SAM."
---

# Teradata Debug SP Generator

Este skill genera Store Procedures de producción para Teradata con infraestructura completa de debug y manejo de errores.

## Cuándo usar este skill

- Transformar queries SQL de desarrollo a SPs de producción
- Agregar logging automático a procedimientos existentes
- Crear infraestructura de monitoreo (tablas debug/error)

## Funciones disponibles

### `generate_debugerror_procedure`
Genera un SP estándar con debug/error para proyectos generales.

```python
from sql_generator import generate_debugerror_procedure

sql = generate_debugerror_procedure(
    nombre_corto_proyecto="portinwinback2024",
    query="SELECT * FROM tabla...",
    tipo_proyecto="mod",  # mod|ana|proc|con
    parametro_fecha="fecha_proceso"
)
```

### `generate_debugerror_procedure_moba2025`
Versión específica para proyectos MOBA2025 con columnas adicionales.

```python
from sql_generator import generate_debugerror_procedure_moba2025

sql = generate_debugerror_procedure_moba2025(
    nombre_corto_proyecto="movilnorecarga2025",
    query="SELECT * FROM tabla...",
    tipo_proyecto="mod",
    parametro_fecha="fecha_proceso"
)
```

## Nomenclatura generada

| Objeto | Formato |
|--------|---------|
| SP Principal | `sp_{tipo}_prod_{nombre}` |
| SP Debug | `sp_{tipo}_prod_debug_{nombre}` |
| Tabla Debug | `debug_{tipo}_prod_{nombre}_hist` |
| Tabla Error | `error_{tipo}_prod_{nombre}_hist` |

## Tipos de proyecto

- `mod` - Modelo
- `ana` - Analítica
- `proc` - Proceso
- `con` - Consumo

## Lo que genera automáticamente

1. **Tablas de soporte**: Crea DDL para tablas `debug_*_hist` y `error_*_hist`
2. **SP de logging**: Procedimiento que inserta en tabla debug
3. **Handler de errores**: `DECLARE EXIT HANDLER FOR SQLEXCEPTION`
4. **Calls de debug**: Inserta llamadas antes de cada `CREATE TABLE`
5. **Marcadores inicio/fin**: Logging de inicio y fin del proceso

## Ejemplo de uso

```python
import sys
sys.path.append('.skills/skills/teradata-debug-sp/scripts')
from sql_generator import generate_debugerror_procedure

query = """
CREATE TABLE proc_tmp_paso1 AS (
    SELECT * FROM fuente
) WITH DATA;

CREATE TABLE proc_tmp_paso2 AS (
    SELECT * FROM proc_tmp_paso1
) WITH DATA;
"""

resultado = generate_debugerror_procedure(
    nombre_corto_proyecto="miproyecto2025",
    query=query,
    tipo_proyecto="mod",
    parametro_fecha="fecha_ejecucion"
)

print(resultado)
```
