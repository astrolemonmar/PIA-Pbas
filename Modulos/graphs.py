import matplotlib.pyplot as plt
from main import *#puse esto para  que al finalizar cada grafica te devuelcva al menu principal, o es deberia de hacer
 
def graficar_compuestos(df_compuestos):
    while True:
        print("Seleccione qué tipo de grafica desea:")
        print("1. Grafico de pastel")
        print("2. Grafico de barras")
        print("3. grfico de dispersión")
 
        tipo_grafico = input("Ingrese el número de la opción deseada: ")
 
        if tipo_grafico == "1":
            propiedad = input("Seleccione qué propiedad de los compuestos desea graficar:\n1. Masa Molecular\n2. LogP\n3. Protones que Acepta\n4. Protones que Cede\n5. Enlaces que rotan\nOpción: ")
            propiedades = {
                "1": "Masa Molecular",
                "2": "LogP",
                "3": "Protones que Acepta",
                "4": "Protones que Cede",
                "5": "Enlaces que rotan"
            }
            propiedad_seleccionada = propiedades.get(propiedad)
            if propiedad_seleccionada:
                graficar_pastel(df_compuestos, propiedad_seleccionada)
            else:
                print("Opción no válida, seleccione una opción que este disponible.")
        elif tipo_grafico == "2":
            propiedad = input("Seleccione qué propiedad de los compuestos desea graficar:\n1. Masa Molecular\n2. LogP\n3. Protones que Acepta\n4. Protones que Cede\n5. Enlaces que rotan\nOpción: ")
            propiedades = {
                "1": "Masa Molecular",
                "2": "LogP",
                "3": "Protones que Acepta",
                "4": "Protones que Cede",
                "5": "Enlaces que rotan"
            }
            propiedad_seleccionada = propiedades.get(propiedad)
            if propiedad_seleccionada:
                graficar_barras(df_compuestos, propiedad_seleccionada)
            else:
                print("Opción no válida, seleccione una opción que este disponible.")
        elif tipo_grafico == "3":
            propiedad = input("Seleccione qué propiedad de los compuestos desea graficar:\n1. Masa Molecular\n2. LogP\n3. Protones que Acepta\n4. Protones que Cede\n5. Enlaces que rotan\nOpción: ")
            propiedades = {
                "1": "Masa Molecular",
                "2": "LogP",
                "3": "Protones que Acepta",
                "4": "Protones que Cede",
                "5": "Enlaces que rotan"
            }
            propiedad_escogida = propiedades.get(propiedad)
            if propiedad_escogida:
                graficar_lineas(df_compuestos, propiedad_escogida)
            else:
                print("Opcin no válida, seleccione una opción que este disponible.")
        else:
            print("Opción no válida. seleccione una opción que este disponible.")
 
 
def graficar_pastel(df_compuestos, propiedad):
    fig, ax = plt.subplots(figsize=(9, 9))
    aqui_se_agrupan_datos = df_compuestos.groupby('Nombre')[propiedad].mean()
    ax.pie(aqui_se_agrupan_datos, labels=aqui_se_agrupan_datos.index, autopct='%1.1f%%')#esto es para dare forma de pstel y mostrar el porcentaje
    ax.set_title(f'Distribución de {propiedad} entre los Compuestos')
    ax.axis('equal')  
    plt.show()
    main()
 
def graficar_barras(df_compuestos, propiedad):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title(f'{propiedad} de los Compuestos')
    ax.set_xlabel('')
    ax.set_ylabel(propiedad)
    ax.set_xticklabels([])  #estoes para eliminar etiquetas en el eje x
    aqui_se_agrupan_datos = df_compuestos.groupby('Nombre')[propiedad].mean()
    colors = plt.cm.get_cmap('tab10', len(aqui_se_agrupan_datos))  #con esto cada barra tiene un color diferente
    for i, (compuesto, promedio) in enumerate(aqui_se_agrupan_datos.items()):
        ax.bar(compuesto, promedio, color=colors(i), label=compuesto)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), shadow=True, ncol=1)
    plt.tight_layout()
    plt.show()
    main()
 
def graficar_lineas(df_compuestos, propiedad):
    fig, ax = plt.subplots(figsize=(8, 5))
    for nombre, datos in df_compuestos.groupby('Nombre'):
        ax.plot(datos.index, datos[propiedad], marker='o', label=nombre)
   
    ax.set_title(f'Gráfico de Líneas de {propiedad}')
    ax.set_xlabel('Compuestos')
    ax.set_ylabel(propiedad)
   
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), shadow=True, ncol=1, fontsize='small')#esto es para que los nombres de los compuestoss aparezcan en un recuadro
   
    ax.set_xticks([])  #esto quita las etiquetas del eje x
   
    plt.tight_layout()
    plt.show()
    main()