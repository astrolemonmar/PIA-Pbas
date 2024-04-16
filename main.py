# Importar librerías
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # No regresar operaciones hasta que cargue el HTML
from selenium.webdriver.support import expected_conditions # 
from selenium.webdriver.common.by import By 

import time
import pandas
import requests
from bs4 import BeautifulSoup

def main():
    # Abrir ZINC en Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')

    driver = webdriver.Chrome(options=options)

    driver.get('https://zinc.docking.org')
if __name__ == "__main__":
    main()