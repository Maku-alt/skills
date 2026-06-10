import pandas as pd
import numpy as np
import logging

def reduce_mem_usage(df, verbose=True):
    """
    Optimiza el uso de memoria de un DataFrame de pandas
    convirtiendo columnas numéricas a tipos de datos más eficientes.

    Parámetros:
    df : pandas.DataFrame
        DataFrame al que se le reducirá el uso de memoria.
    verbose : bool, opcional (por defecto True)
        Si es True, imprime la reducción de memoria en Mb y porcentaje.

    Retorna:
    df : pandas.DataFrame
        DataFrame con tipos de datos optimizados.
    """
    try:
        # Lista de tipos numéricos a considerar para optimización.
        numerics = ['int8', 'int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        
        # Calcular uso de memoria inicial en megabytes.
        start_mem = df.memory_usage().sum() / 1024**2

        # Iterar sobre cada columna del DataFrame.
        for col in df.columns:
            # Obtener el tipo de dato de la columna.
            col_type = df[col].dtypes

            # Solo se procesan las columnas de tipo numérico.
            if col_type in numerics:
                # Obtener el valor mínimo y máximo de la columna.
                c_min = df[col].min()
                c_max = df[col].max()

                # Si la columna es de tipo entero...
                if str(col_type)[:3] == 'int':
                    # Convertir a int8 si los valores caben en su rango.
                    if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                        df[col] = df[col].astype(np.int8)
                    # Sino, probar con int16.
                    elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                        df[col] = df[col].astype(np.int16)
                    # Sino, probar con int32.
                    elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                        df[col] = df[col].astype(np.int32)
                    # Sino, se mantiene o asigna a int64.
                    elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                        df[col] = df[col].astype(np.int64)
                else:
                    # Para columnas de tipo flotante, convertir a float32 si es posible.
                    if c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                        df[col] = df[col].astype(np.float32)
                    else:
                        # Sino, se asigna a float64.
                        df[col] = df[col].astype(np.float64)

        # Calcular el uso de memoria final tras la optimización.
        end_mem = df.memory_usage().sum() / 1024**2

        # Si verbose es True, imprimir el ahorro de memoria en Mb y en porcentaje.
        if verbose:
            logging.info('Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction)'.format(
                end_mem, 100 * (start_mem - end_mem) / start_mem))
        
        # Retornar el DataFrame optimizado.
        return df

    except Exception as e:
        # En caso de error, se imprime un mensaje y se lanza la excepción.
        print(f"Error en reduce_mem_usage: {e}")
        raise e
