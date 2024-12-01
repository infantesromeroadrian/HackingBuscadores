from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class SeleniumSearcher:
    """Clase para realizar búsquedas en Google usando Selenium WebDriver."""

    def __init__(self):
        """Inicializa el navegador Firefox con opciones configuradas."""
        self.browser = None

    def initialize_browser(self):
        """Configura e inicializa el navegador."""
        service = Service(GeckoDriverManager().install())
        options = webdriver.FirefoxOptions()
        options.add_argument('--disable-extensions')
        options.add_argument('--no-sandbox')
        # Puedes agregar `--headless` si deseas ejecutar en modo sin interfaz gráfica
        self.browser = webdriver.Firefox(service=service, options=options)

    def perform_search(self, query):
        """Realiza una búsqueda en Google con Selenium."""
        try:
            self.browser.get('http://www.google.com')
            self.accept_cookies()
            search_box = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.NAME, 'q'))
            )
            search_box.send_keys(query + Keys.ENTER)
            time.sleep(3)
            return self.extract_results()
        except Exception as e:
            print(f"Error durante la búsqueda con Selenium: {e}")
            return []
        finally:
            self.browser.quit()

    def accept_cookies(self):
        """Acepta las cookies si aparecen en la página principal de Google."""
        try:
            accept_button = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.ID, 'L2AGLb'))
            )
            accept_button.click()
        except Exception:
            pass  # No siempre aparecen cookies, ignorar si no están presentes.

    def extract_results(self):
        """Extrae resultados de la búsqueda y los devuelve como una lista de diccionarios."""
        results = []
        try:
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.g'))
            )
            result_elements = self.browser.find_elements(By.CSS_SELECTOR, 'div.g')
            for element in result_elements:
                try:
                    title = element.find_element(By.CSS_SELECTOR, 'h3').text
                    link = element.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    description = element.find_element(By.CSS_SELECTOR, 'div.VwiC3b').text
                    results.append({
                        "title": title,
                        "link": link,
                        "description": description,
                    })
                except Exception:
                    continue
        except Exception as e:
            print(f"Error al extraer resultados: {e}")
        return results
