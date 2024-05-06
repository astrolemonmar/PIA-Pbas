import matplotlib.pyplot as plt

def graficar_estadisticas(estadisticas):
    print("Seleccione el tipo de gráfico que desea generar:")
    print("1. Gráfico de barras")
    print("2. Gráfico de líneas")
    print("3. Gráfico de dispersión")
    
    tipo_grafico = input("Ingrese el número de la opción deseada: ")
    
    if tipo_grafico not in ["1", "2", "3"]:
        print("Opción no válida. Por favor, seleccione una opción válida.")
        return
    
    variables = estadisticas['Variable']
    
    print("Seleccione la variable que desea graficar:")
    for i, variable in enumerate(variables):
        print(f"{i + 1}. {variable}")
    
    opcion = input("Ingrese el número de la opción deseada: ")
    
    try:
        opcion = int(opcion)
        if opcion < 1 or opcion > len(variables):
            print("Opción no válida. Por favor, seleccione una opción válida.")
            return
    except ValueError:
        print("Por favor, ingrese un número válido.")
        return
    
    variable_seleccionada = variables[opcion - 1]
    
    cantidad_datos = estadisticas['Cantidad de datos'][opcion - 1]
    promedio = estadisticas['Promedio de la variable'][opcion - 1]
    desviacion_estandar = estadisticas['Desviación estandar'][opcion - 1]
    valor_minimo = estadisticas['Valor mínimo'][opcion - 1]
    cuartil_1 = estadisticas['Percentil 25 o Cuartil 1'][opcion - 1]
    mediana = estadisticas['Percentil 50 o Mediana'][opcion - 1]
    cuartil_3 = estadisticas['Percentil 75 o Cuartil 3'][opcion - 1]
    valor_maximo = estadisticas['Valor máximo'][opcion - 1]
    
    if tipo_grafico == "1":  # Gráfico de barras
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.bar(['Cantidad de datos', 'Promedio', 'Desviación estándar', 'Mínimo', 'Cuartil 1', 'Mediana', 'Cuartil 3', 'Máximo'],
               [cantidad_datos, promedio, desviacion_estandar, valor_minimo, cuartil_1, mediana, cuartil_3, valor_maximo])
        ax.set_title(f'Estadísticas de {variable_seleccionada}')
    elif tipo_grafico == "2":  # Gráfico de líneas
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(['Cantidad de datos', 'Promedio', 'Desviación estándar', 'Mínimo', 'Cuartil 1', 'Mediana', 'Cuartil 3', 'Máximo'],
                [cantidad_datos, promedio, desviacion_estandar, valor_minimo, cuartil_1, mediana, cuartil_3, valor_maximo], marker='o')
        ax.set_title(f'Estadísticas de {variable_seleccionada}')
        ax.set_xlabel('Estadísticas')
        ax.set_ylabel('Valor')
    elif tipo_grafico == "3":  # Gráfico de dispersión
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.scatter(['Cantidad de datos', 'Promedio', 'Desviación estándar', 'Mínimo', 'Cuartil 1', 'Mediana', 'Cuartil 3', 'Máximo'],
                   [cantidad_datos, promedio, desviacion_estandar, valor_minimo, cuartil_1, mediana, cuartil_3, valor_maximo])
        ax.set_title(f'Estadísticas de {variable_seleccionada}')
        ax.set_xlabel('Estadísticas')
        ax.set_ylabel('Valor')

    plt.tight_layout()
    plt.show()