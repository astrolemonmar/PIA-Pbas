# Importar librerías
import time
import pandas
import requests
from bs4 import BeautifulSoup
from proof_mods import *

def main():
    print("Bienvenido a PUBCHEM search.")
    opcion = menu_principal()
    while opcion:
        print("")
        opcion = menu_principal()
if __name__ == "__main__":
    main()  