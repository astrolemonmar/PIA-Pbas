import json
import pandas as pd
import os

def tomar_datos(comp_name_list, carpeta_destino):
    datos_compuestos = []
    # Leer la información de los archivos de texto y agregarla al DataFrame
    for comp_name in comp_name_list:
        ruta_archivo = os.path.join(carpeta_destino, f"{comp_name}.txt")  # Construir la ruta completa
        with open(ruta_archivo, "r") as file:
            data_json = json.load(file)
            nombre = str(obtener_valor_por_clave(data_json, "Traditional", "sval"))
            masa_molecular = obtener_valor_por_clave(data_json, "Molecular Weight", "sval")
            if obtener_valor_por_clave(data_json, "Molecular Weight", "sval") == None:
                masa_molecular = None
            else:
                masa_molecular = float(masa_molecular)
            logp = obtener_valor_por_clave(data_json, "Log P", "fval")
            if obtener_valor_por_clave(data_json, "Log P", "fval") == None:
                logp = None
            else:
                logp = float(logp)
            protones_acepta = obtener_valor_por_clave(data_json, "Hydrogen Bond Acceptor", "ival")
            if obtener_valor_por_clave(data_json, "Hydrogen Bond Acceptor", "ival") == None:
                protones_acepta = None
            else:
                protones_acepta = int(protones_acepta)
            protones_cede = obtener_valor_por_clave(data_json, "Hydrogen Bond Donor", "ival")
            if obtener_valor_por_clave(data_json, "Hydrogen Bond Donor", "ival")== None:
                protones_cede = None
            else:
                protones_cede = int(protones_cede)
            enlances_rotables = obtener_valor_por_clave(data_json, "Rotatable Bond", "ival")
            if obtener_valor_por_clave(data_json, "Rotatable Bond", "ival") == None:
                enlances_rotables = None
            else:
                enlaces_rotables = int(enlances_rotables)
            datos_compuestos.append({'Nombre': nombre,
                                     'Masa Molecular': masa_molecular,
                                     'LogP': logp,
                                     'Protones que Acepta': protones_acepta,
                                     'Protones que Cede': protones_cede,
                                     'Enlaces que rotan': enlances_rotables})
    print(f"Datos del compuesto", datos_compuestos)
    return datos_compuestos


def obtener_valor_por_clave(data_json, clave_buscada, clave_valor):
    # Buscar la clave buscada dentro de la estructura JSON
    for prop in data_json['PC_Compounds'][0]['props']:
        if prop['urn']['label'] == clave_buscada:
            # Si se encuentra la clave buscada, obtener el valor asociado
            valor = prop['value'].get(clave_valor)
            return valor
        elif 'name' in prop['urn'] and prop['urn']['name'] == clave_buscada:
            # Si se encuentra la clave buscada, obtener el valor asociado
            valor = prop['value'].get(clave_valor)
            return valor
    return None

def generar_estadisticas(df_compuestos):
    calculos = {
        'Variable': ['Masa Molecular', 'LogP', 'Protones que Acepta', 'Protones que Cede', 'Enlaces que rotan'],
        'Cantidad de datos': [df_compuestos['Masa Molecular'].count(), df_compuestos['LogP'].count(),
                  df_compuestos['Protones que Acepta'].count(), df_compuestos['Protones que Cede'].count(), df_compuestos['Enlaces que rotan'].count()],
        'Promedio de la variable': [df_compuestos['Masa Molecular'].mean(), df_compuestos['LogP'].mean(),
                 df_compuestos['Protones que Acepta'].mean(), df_compuestos['Protones que Cede'].mean(), df_compuestos['Enlaces que rotan'].mean()],
        'Desviación estandar': [df_compuestos['Masa Molecular'].std(), df_compuestos['LogP'].std(),
                df_compuestos['Protones que Acepta'].std(), df_compuestos['Protones que Cede'].std(), df_compuestos['Enlaces que rotan'].std()],
        'Valor mínimo': [df_compuestos['Masa Molecular'].min(), df_compuestos['LogP'].min(),
                df_compuestos['Protones que Acepta'].min(), df_compuestos['Protones que Cede'].min(), df_compuestos['Enlaces que rotan'].min()],
        'Percentil 25 o Cuartil 1': [df_compuestos['Masa Molecular'].quantile(0.25), df_compuestos['LogP'].quantile(0.25),
                df_compuestos['Protones que Acepta'].quantile(0.25), df_compuestos['Protones que Cede'].quantile(0.25), df_compuestos['Enlaces que rotan'].quantile(0.25)],
        'Percentil 50 o Mediana': [df_compuestos['Masa Molecular'].quantile(0.5), df_compuestos['LogP'].quantile(0.5),
                df_compuestos['Protones que Acepta'].quantile(0.5), df_compuestos['Protones que Cede'].quantile(0.5), df_compuestos['Enlaces que rotan'].quantile(0.5)],
        'Percentil 75 o Cuartil 3': [df_compuestos['Masa Molecular'].quantile(0.75), df_compuestos['LogP'].quantile(0.75),
                df_compuestos['Protones que Acepta'].quantile(0.75), df_compuestos['Protones que Cede'].quantile(0.75), df_compuestos['Enlaces que rotan'].quantile(0.75)],
        'Valor máximo': [df_compuestos['Masa Molecular'].max(), df_compuestos['LogP'].max(),
                df_compuestos['Protones que Acepta'].max(), df_compuestos['Protones que Cede'].max(), df_compuestos['Enlaces que rotan'].max()],
    }
    return calculos