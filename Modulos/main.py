# Importar librerías
from consultas_mods import *

def main():
    print("Bienvenido a PUBCHEM search.")
    opcion = menu()
    while opcion:
        print("")
        opcion = menu()
if __name__ == "__main__":
    main()  