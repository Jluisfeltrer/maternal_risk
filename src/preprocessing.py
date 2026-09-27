def convertir_farenheit_a_celsius(df, columna = 'BodyTemp'):
    df = df.copy()
    df[columna] = (df[columna] - 32) * 5/9
    return df

def excluir_valores_invalidos(df, columna, umbral_min):
    filas_excluidas = df[df[columna] < umbral_min]
    n = len(filas_excluidas)
    print(f"Se excluyeron {n} filas por valores fisiologicamente imposibles en '{columna}' (< {umbral_min}).")
    df_limpio = df[df[columna] >= umbral_min].copy()
    return df_limpio, filas_excluidas

def crear_indicador_fiebre(df, umbral=37.2):
    df=df.copy()
    df['tiene_fiebre'] = (df['BodyTemp'] > umbral).astype(int)
    return df
