from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import requests

class ConsultaAPI:
    def __init__(self, url_base):
        self.url_base = url_base
    def realizar_consulta(self, comp_name):
        url_comp = f"{self.url_base}/compound/name/{comp_name}/cids/JSON"
        response = requests.get(url_comp)
        if response.status_code == 200:
            data = response.json()
            cid = data["IdentifierList"]["CID"][0]
            #print(data)
            return cid
        else:
                print("Error en la solicitud:", response.status_code)
                if response.status_code == 400:
                    print("PUGREST.BadRequest \nRequest is improperly formed (syntax error in the URL, POST body, etc.)")
                elif response.status_code == 404:
                    print("PUGREST.NotFound\nThe input record was not found (e.g. invalid CID)")
                elif response.status_code == 405:
                    print("PUGREST.NotAllowed \nRequest not allowed (such as invalid MIME type in the HTTP Accept header)")
                elif response.status_code == 504:
                    print("PUGREST.Timeout \nThe request timed out, from server overload or too broad a request")
                elif response.status_code == 503:
                    print("PUGREST.ServerBusy	Too many requests or server is busy, retry later")
                elif response.status_code == 501:
                    print("PUGREST.Unimplemented \nThe requested operation has not (yet) been implemented by the server")
                elif response.status_code == 500:
                    print("PUGREST.ServerError \nSome problem on the server side (such as a database server down, etc.)\n   or\n")
                    print("PUGREST.Unknown \nAn unknown error occurred")

def obtener_informacion_compuesto(cid):
    base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
    url = f"{base_url}/compound/cid/{cid}/JSON"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
            # print data
        return data
    #else:
    #    print("Error en la solicitud:", response.status_code)

def menu_principal():
    print("Bienvenido a PUBCHEM search.")
    print("1. Consultas web")
    print("2. Consultas de registros")
    print("3. Estadísticas")
    print("4. Gráficas")
    print("5. Borrar todo")
    print("6. Salir")

    opcion = input("Ingrese el número de la opción deseada: ")

    if opcion == "1":
        url_base = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
        consulta = ConsultaAPI(url_base)

        comp_name = input("Ingrese el nombre del compuesto a buscar: ")
        cid = consulta.realizar_consulta(comp_name)

        data_json = obtener_informacion_compuesto(cid)
        data_str = json.dumps(data_json, indent=4)

        with open("info_compuesto.txt", "w") as file:
            file.write(data_str)
    else:
        print("Opción no válida. Por favor, seleccione una opción válida.")
        menu_principal()
