def resumen_dimensiones(df):
    print(f"El numero de filas es: {df.shape[0]}")
    print(f"El numero de columnas es: {df.shape[1]}")
    print("\nTipos de datos por columna: ")
    print(df.dtypes)