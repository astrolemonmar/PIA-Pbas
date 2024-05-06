import json
import os
import requests
import openpyxl
import matplotlib as plt 
from openpyxl import load_workbook
import pandas as pd
from estadísticas import *
from graficas import *

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
    try:
        opcion = int(opcion)
        if opcion == 1:
            try:
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
                    print(f"Archivo {comp_name} guardado con éxito!")

            except requests.exceptions.RequestException:
                print("No se puede conectar a Internet. Por favor, verifica tu conexión y vuelve a intentarlo.")
                if len(comp_name_list) > 0:
                    print("O consulta tus archivos anteriormente guardados.")
                    j = 0
                    for i in comp_name_list:
                        j += 1
                        print("f{j}" ,i)
        elif opcion == 2:
            if len(comp_name_list) > 0:
                pd.set_option('display.max_rows', None)
                pd.set_option('display.max_columns', None)
                for i in comp_name_list:
                    with open (str(i)+".txt"):        
                        data = pd.read_json(str(i)+".txt")
                    print(data)
            else:
                print("Aun no hay archivos descargados.")
            #abrir_xlsx(comp_name_list)
        
        elif opcion == 3:
            pass
        
        elif opcion == 4:
            if len(comp_name_list) == 0:
                print("No hay datos disponibles. Realiza consultas web primero.")
            else:
                df_compuestos = pd.DataFrame(tomar_datos(comp_name_list))
                estadisticas = generar_estadisticas(df_compuestos)
                graficar_estadisticas(estadisticas)
        
        elif opcion == 5:
            borrar_todo()
        elif opcion == 6:
            borrar_todo()
            opcion = False
            return opcion
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")
            menu()
        return opcion
    except ValueError:
        print("Opción no válida. Por favor, seleccione una opción válida.")
        menu()

class ConsultaAPI:
    def __init__(self, url_base):
        self.url_base = url_base

    def realizar_consulta(self, comp_name):
        url_comp = f"{self.url_base}/compound/name/{comp_name}/cids/JSON"

        try:
            response = requests.get(url_comp)
            response.raise_for_status()
            data = response.json()
            cid = data["IdentifierList"]["CID"][0]
            return cid
        except requests.exceptions.RequestException:
            response = requests.get(url_comp)
            error_messages = {
                400: "PUGREST.BadRequest \nLa solicitud está mal formada (error de sintaxis en la URL, cuerpo POST, etc.)",
                404: "PUGREST.NotFound\nEl registro de entrada no fue encontrado (por ejemplo, CID inválido)",
                405: "PUGREST.NotAllowed \nSolicitud no permitida (como tipo MIME inválido en el encabezado HTTP Accept)",
                504: "PUGREST.Timeout \nLa solicitud ha expirado debido a una sobrecarga del servidor o a una solicitud demasiado amplia",
                503: "PUGREST.ServerBusy\nDemasiadas solicitudes o el servidor está ocupado, intente nuevamente más tarde",
                501: "PUGREST.Unimplemented \nLa operación solicitada aún no ha sido implementada por el servidor",
                500: "PUGREST.ServerError \nAlgun problema en el lado del servidor (como un servidor de base de datos caído, etc.)\n   o\n PUGREST.Unknown \nSe ha producido un error desconocido"
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
        return data



def borrar_todo():
    global comp_name_list
    for comp_name in (comp_name_list):
        if os.path.exists(str(comp_name)+".txt"):
            os.remove(str(comp_name)+".txt")
            print(f"El archivo {str(comp_name)+".txt"} ha sido borrado exitosamente.")
        else:
            pass

