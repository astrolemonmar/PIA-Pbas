# Importar librerías
from Modulos import consultas_mods

def main():
    print("Bienvenido a PUBCHEM search.")
    opcion = consultas_mods.menu()
    while opcion:
        print("")
        opcion = consultas_mods.menu()
def menu_cm():
    pass
if __name__ == "__main__":
    main()  