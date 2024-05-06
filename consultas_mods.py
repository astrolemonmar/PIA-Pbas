import json
import os
import requests
import openpyxl
import matplotlib as plt 

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b)
        s = s.casefold()
    return s

comp_name_list = [ ] #lista que almacena todos los nombres de compuestos que buscamos
def menu():
    global comp_name_list
    print("1. Consultas web: Descarga información del compuesto que desees")
    print("2. Consultas de registros: Consulta la información descargada")
    print("3. Estadísticas")
    print("4. Gráficas")
    print("5. Borrar todo")
    print("6. Salir")

    opcion = input("Ingrese el número de la opción deseada: ")

    if opcion == "1":
        url_base = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
        consulta = ConsultaAPI(url_base)

        comp_name = input("Ingrese el nombre del compuesto a buscar: ")
        # Funcion que quita tildes y regresa en lower case
        comp_name = normalize(comp_name)
        cid = consulta.realizar_consulta(comp_name)

        data_json = obtener_informacion_compuesto(cid)
        if data_json is None:
            print("Archivo no guardado")
        else:
            comp_name_list.append(comp_name)
            data_str = json.dumps(data_json, indent=4)
            with open(str(comp_name)+".txt", "w") as file:
                file.write(data_str)
    elif opcion == "5":
        borrar_todo()
    elif opcion == "6":
        borrar_todo()
        opcion = False
        return opcion
    else:
        print("Opción no válida. Por favor, seleccione una opción válida.")
        menu()
    return opcion

class ConsultaAPI:
    def __init__(self, url_base):
        self.url_base = url_base

    def realizar_consulta(self, comp_name):
        url_comp = f"{self.url_base}/compound/name/{comp_name}/cids/JSON"

        try:
            response = requests.get(url_comp)
            response.raise_for_status() #raises http error if one ocures
            data = response.json()
            cid = data["IdentifierList"]["CID"][0]
            #print(data)
            return cid
        except requests.exceptions.RequestException:
            response = requests.get(url_comp)
            error_messages = {
                400: "PUGREST.BadRequest \nRequest is improperly formed (syntax error in the URL, POST body, etc.)",
                404: "PUGREST.NotFound\nThe input record was not found (e.g. invalid CID)",
                405: "PUGREST.NotAllowed \nRequest not allowed (such as invalid MIME type in the HTTP Accept header)",
                504: "PUGREST.Timeout \nThe request timed out, from server overload or too broad a request",
                503: "PUGREST.ServerBusy	Too many requests or server is busy, retry later",
                501: "PUGREST.Unimplemented \nThe requested operation has not (yet) been implemented by the server",
                500: "PUGREST.ServerError \nSome problem on the server side (such as a database server down, etc.)\n   or\n PUGREST.Unknown \nAn unknown error occurred"
            }
            print("Error en la solicitud:", response.status_code, error_messages[response.status_code])
            return None
 

def obtener_informacion_compuesto(cid):
    if cid is None:
        return None
    
    base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
    url = f"{base_url}/compound/cid/{cid}/JSON"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
            # print data
        return data
    #else:
    #    print("Error en la solicitud:", response.status_code)

def borrar_todo():
    global comp_name_list
    for comp_name in (comp_name_list):
        if os.path.exists(str(comp_name)+".txt"):
            os.remove(str(comp_name)+".txt")
            print(f"El archivo {str(comp_name)+".txt"} ha sido borrado exitosamente.")
        """
        else:
            print(f"El archivo {str(comp_name)+".txt"} no existe.")
        """

def graficar_estadisticas(estadisticas):
    variables = estadisticas['Variable']
    cantidad_datos = estadisticas['Cantidad de datos']
    promedio = estadisticas['Promedio de la variable']
    desviacion_estandar = estadisticas['Desviación estandar']
    valor_minimo = estadisticas['Valor mínimo']
    cuartil_1 = estadisticas['Percentil 25 o Cuartil 1']
    mediana = estadisticas['Percentil 50 o Mediana']
    cuartil_3 = estadisticas['Percentil 75 o Cuartil 3']
    valor_maximo = estadisticas['Valor máximo']
 
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))
 
    for i, ax in enumerate(axes.flatten()):
        if i < len(variables):
            ax.bar(['Cantidad de datos', 'Promedio', 'Desviación estándar', 'Mínimo', 'Cuartil 1', 'Mediana', 'Cuartil 3', 'Máximo'],
                   [cantidad_datos[i], promedio[i], desviacion_estandar[i], valor_minimo[i], cuartil_1[i], mediana[i], cuartil_3[i], valor_maximo[i]])
            ax.set_title(f'Estadísticas de {variables[i]}')
 
    plt.tight_layout()
    plt.show()