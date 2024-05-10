import json
import os
import requests
import pandas as pd
from Modulos import stats
from Modulos import graphs
from googletrans import Translator

comp_name_list = [ ]
excel_list = [ ]
graph_list = [ ]

file_request = "Reportes de Consulta Api"
file_report = "Reportes de datos numericos"
file_graph = "Graficas"

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

def translate_compound(compound_name):
    try:
        translation_response = requests.get(f"http://www.google.com")
        translation_response.raise_for_status()
        translator = Translator()
        translated_text = translator.translate(compound_name, src="es", dest="en")
        return translated_text.text
    except requests.exceptions.RequestException:
        return compound_name

class RequestAPI:
    def __init__(self, url_base):
        self.url_base = url_base

    def to_request(self, comp_name):
        url_comp = f"{self.url_base}/compound/name/{comp_name}/cids/JSON"

        try:
            response = requests.get(url_comp)
            response.raise_for_status()
            data = response.json()
            cid = data["IdentifierList"]["CID"][0] #CID <- Chemical Identifier
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

def get_info(cid):
    try:
        if cid is None:
            return None
        
        base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
        url = f"{base_url}/compound/cid/{cid}/JSON"
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
    except requests.exceptions.RequestException as e:
        return None
    
def txt_files():
    try:
        url_base = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
        consulta = RequestAPI(url_base)
        comp_name = input("Nombre del compuesto: ")
        comp_name = translate_compound(comp_name)               
        comp_name = normalize(comp_name)
        cid = consulta.to_request(comp_name)

        data_json = get_info(cid)
        if data_json is None:
            pass
        else:
            carpeta_txt = "Reportes de Consulta Api"
            comp_name_list.append(comp_name)
            data_str = json.dumps(data_json, indent=4)
            ruta_archivo = os.path.join(carpeta_txt, f"{comp_name}.txt")
            with open(ruta_archivo, "w") as archivo:
                archivo.write(data_str)
                print(f"Archivo guardado como: {comp_name}.txt")

    except requests.exceptions.RequestException:
        print("No se puede conectar a Internet. Por favor, verifica tu conexión y vuelve a intentarlo.")
        if len(comp_name_list) > 0:
            print("O consulta tus archivos anteriormente guardados.")
            j = 0
            for i in comp_name_list:
                j += 1
                print(f"\t{j}." ,i)

def delate(path_file_request, path_file_report, path_file_graphs):
    global comp_name_list, excel_list, graph_list
    if len(comp_name_list) > 0:
        for comp_name in (comp_name_list):
            path_file = os.path.join(path_file_request, f"{comp_name}.txt")
            if os.path.exists(path_file):
                os.remove(path_file)
        comp_name_list = []

        for excel_files in (excel_list):
                path_file = os.path.join(path_file_report, f"{excel_files}.xlsx")
                if os.path.exists(path_file):
                    os.remove(path_file)
        excel_list = []

        graph_list = graphs.graphs_list_return()
        for graph in (graph_list):
            path_file = os.path.join(path_file_graphs, f"{graph}")
            if os.path.exists(path_file):
                os.remove(path_file)
        return True
    else:
        return False

def download(path_file_request):
    print("Consulta tus archivos anteriormente guardados.")
    if len(comp_name_list) > 0:
        j = 0
        for i in comp_name_list:
            j += 1
            print(f"\t{j}." ,i)

        try:
            comp_name_i = int(input("Selecciona un archivo: ")) - 1
            if 0 <= comp_name_i < len(comp_name_list):
                comp_file_name = comp_name_list[comp_name_i]
                path_file = os.path.join(path_file_request, f"{comp_file_name}.txt")
                
                try:
                    with open(path_file, "r") as archivo:
                        contenido = archivo.read()
                        data = json.loads(contenido)
                        
                    compuestos = data.get("PC_Compounds", [])
                    if compuestos:
                        for compuesto in compuestos:
                            print("ID del compuesto:", compuesto["id"]["id"]["cid"])
                            print("Fórmula molecular:", compuesto["props"][16]["value"]["sval"])
                            print("Peso molecular:", compuesto["props"][15]["value"]["sval"])
                    else:
                        print("No se encontraron datos de compuestos en el archivo.")
                
                except FileNotFoundError:
                    print("El archivo seleccionado no existe.")
                except ValueError:
                    print("El archivo seleccionado no contiene datos válidos.")
            else:
                print("Selecciona un número de archivo válido.")
        
        except ValueError:
            print("Por favor, ingresa un número válido para seleccionar un archivo.")

    else:
        print("No hay datos disponibles. Realiza consultas web primero.")
        return None


def menu():
    global comp_name_list, excel_list
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
            txt_files()

        elif opcion == 2:
            answer = download(file_request)
            if answer is None:
                pass

        elif opcion == 3:
            if len(comp_name_list) == 0:
                print("No hay datos disponibles. Realiza consultas web primero.")
            else:
                nombre_del_archivo = str(input("Nombre del nuevo archivo Excel: "))
                excel_list.append(nombre_del_archivo)
                df_compuestos = pd.DataFrame(stats.tomar_datos(comp_name_list, file_request))
                estadisticas = stats.generar_estadisticas(df_compuestos)
                df_estadisticas = pd.DataFrame(estadisticas)
                with pd.ExcelWriter(os.path.join("Reportes de datos numericos", nombre_del_archivo + ".xlsx")) as writer:
                    df_compuestos.to_excel(writer, sheet_name="Datos Compuestos", index=False)
                    df_estadisticas.to_excel(writer, sheet_name="Datos Cálculos", index=False)
                print(f"Los datos y cálculos se han guardado en el archivo Excel: '{nombre_del_archivo}.xlsx' ")

        elif opcion == 4:
            if len(comp_name_list) == 0:
                print("No hay datos disponibles. Realiza consultas web primero.")
            else:
                df_compuestos = pd.DataFrame(stats.tomar_datos(comp_name_list,file_request))
                graphs.graficar_compuestos(df_compuestos)

        elif opcion == 5:
            answer = delate(file_request,file_report,file_graph)
            if answer == True:
                print("Archivos borrados exitosamente")
            else:
                print("No existen archivos registrados para borrar")

        elif opcion == 6:
            delate(file_request,file_report,file_graph)
            print("Gracias por utilizar PubChem search c:")
            opcion = False
            
        else:
            print("Opción no válida. Por favor, selecciona una opción válida.")
            menu()
        return opcion
    except ValueError:
        print("Opción no válida. Por favor, selecciona una opción válida.")
        menu()