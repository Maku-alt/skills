---
name: pandas-optimizer
description: "Optimiza el uso de memoria de DataFrames de pandas. Usar cuando el agente trabaje con datasets grandes y necesite reducir el consumo de memoria convirtiendo columnas numéricas a tipos más eficientes (int8, int16, float32, etc.)."
---

# Pandas Memory Optimizer

Optimiza DataFrames de pandas reduciendo el uso de memoria mediante conversión inteligente de tipos de datos.

## Cuándo usar

- Datasets grandes que consumen mucha RAM
- Antes de operaciones costosas en memoria
- Al cargar múltiples DataFrames simultáneamente

## Uso

```python
import sys
sys.path.append('.skills/skills/pandas-optimizer/scripts')
from data_utils import reduce_mem_usage

import pandas as pd

df = pd.read_csv('archivo_grande.csv')
df_optimizado = reduce_mem_usage(df, verbose=True)
# Output: Mem. usage decreased to 45.23 Mb (67.5% reduction)
```

## Función `reduce_mem_usage`

```python
reduce_mem_usage(df, verbose=True)
```

**Parámetros:**
- `df`: DataFrame a optimizar
- `verbose`: Si True, imprime la reducción de memoria

**Retorna:** DataFrame con tipos optimizados

## Qué hace

1. Analiza cada columna numérica (int/float)
2. Detecta el rango de valores (min/max)
3. Convierte al tipo más pequeño posible:
   - `int64` → `int8/int16/int32`
   - `float64` → `float32`
4. Reporta la reducción en MB y porcentaje
