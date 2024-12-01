

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def main():
    """
    Automación de búsqueda en Google con Selenium WebDriver.
    """
    # Configuración inicial para Firefox WebDriver
    service = Service(GeckoDriverManager().install())
    options = webdriver.FirefoxOptions()

    # Ejecución en modo headless (sin interfaz gráfica, opcional)
    # options.add_argument('--headless')

    # Desactiva extensiones o configuraciones adicionales
    options.add_argument('--disable-extensions')
    options.add_argument('--no-sandbox')

    try:
        # Inicializa el navegador
        browser = webdriver.Firefox(service=service, options=options)

        # Accede a la página principal de Google
        browser.get('http://www.google.com')

        # Paso 1: Manejar el botón de cookies (si existe)
        accept_cookies(browser)

        # Paso 2: Realizar una búsqueda en Google
        query = 'Adrian Infantes Romero'
        perform_search(browser, query)

        # Paso 3: Extraer los resultados de búsqueda
        extract_results(browser)

    except Exception as e:
        print(f"Error en la ejecución: {e}")

    finally:
        # Cierra el navegador
        if 'browser' in locals():
            browser.quit()

def accept_cookies(browser):
    """
    Acepta las cookies en la página principal de Google.

    Args:
        browser (webdriver.Firefox): Instancia del navegador para interactuar con la web.
    """
    try:
        # Espera hasta que el botón de aceptar cookies sea clickeable y luego haz clic
        accept_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, 'L2AGLb'))
        )
        accept_button.click()
        print("Cookies aceptadas.")
    except Exception as e:
        print("No se encontraron cookies o hubo un error: ", e)

def perform_search(browser, query):
    """
    Realiza una búsqueda en Google enviando una consulta al cuadro de texto de búsqueda.

    Args:
        browser (webdriver.Firefox): Instancia del navegador para interactuar con la web.
        query (str): Texto de la consulta de búsqueda.
    """
    try:
        # Encuentra el cuadro de búsqueda y escribe la consulta seguida de Enter
        search_box = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.NAME, 'q'))
        )
        search_box.send_keys(query + Keys.ENTER)
        print(f"Búsqueda realizada con el término: {query}")
        time.sleep(3)  # Tiempo para que los resultados se carguen completamente
    except Exception as e:
        print("Error al realizar la búsqueda: ", e)

def extract_results(browser):
    """
    Extrae los títulos, enlaces y descripciones de los primeros resultados de búsqueda.

    Args:
        browser (webdriver.Firefox): Instancia del navegador para interactuar con la web.
    """
    try:
        # Espera hasta que los resultados de búsqueda estén presentes
        WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.g'))
        )

        # Encuentra todos los contenedores de resultados (div con clase 'g')
        results = browser.find_elements(By.CSS_SELECTOR, 'div.g')
        print(f"Se encontraron {len(results)} resultados.")

        for result in results:
            try:
                # Extrae el título, enlace y descripción de cada resultado
                title = result.find_element(By.CSS_SELECTOR, 'h3').text
                link = result.find_element(By.TAG_NAME, 'a').get_attribute('href')
                description = result.find_element(By.CSS_SELECTOR, 'div.VwiC3b').text
                print(f'Título: {title}\nEnlace: {link}\nDescripción: {description}\n')
            except Exception:
                print("Un elemento del resultado no pudo ser extraído.")
                continue
    except Exception as e:
        print("Error al extraer resultados: ", e)

if __name__ == "__main__":
    main()

