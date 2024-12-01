import requests
import re
from rich.console import Console
from rich.panel import Panel


class GoogleDorking:
    """Clase para realizar búsquedas Dorking usando la API personalizada de Google."""

    def __init__(self, api_key, engine_id):
        """
        Inicializa la clase con la clave de API y el motor de búsqueda.

        Args:
            api_key (str): Clave de API de Google
            engine_id (str): ID del motor de búsqueda personalizado
        """
        self.api_key = api_key
        self.engine_id = engine_id
        self.console = Console()

    def search(self, query, site=None, start_page=1, pages=1, lang="lang_en"):
        """
        Realiza una búsqueda en Google utilizando la API.

        Args:
            query (str): Consulta de búsqueda
            site (str, optional): Sitio específico donde buscar
            start_page (int, optional): Página inicial
            pages (int, optional): Número de páginas a buscar
            lang (str, optional): Idioma de búsqueda

        Returns:
            list: Lista de resultados procesados
        """
        self.console.print(Panel.fit(
            f"[bold cyan]Iniciando búsqueda[/bold cyan]\n"
            f"[yellow]Query:[/yellow] {query}\n"
            f"[yellow]Páginas:[/yellow] {pages}",
            title="Google Dorking"
        ))

        final_results = []
        results_per_page = 10  # Google muestra 10 resultados por página

        for page in range(pages):
            start_index = (start_page - 1) * results_per_page + 1 + (page * results_per_page)
            query_with_site = f'{query} site:{site}' if site else query
            url = (
                f"https://www.googleapis.com/customsearch/v1?key={self.api_key}&cx={self.engine_id}"
                f"&q={query_with_site}&start={start_index}&lr={lang}"
            )

            self.console.print(f"[cyan]→[/cyan] Consultando página {page + 1}...")

            try:
                response = requests.get(url)
                response.raise_for_status()  # Lanza una excepción para códigos de error HTTP

                data = response.json()
                results = data.get("items", [])
                final_results.extend(self.custom_results(results))

                self.console.print(f"[green]✓[/green] Página {page + 1} procesada")

            except requests.exceptions.RequestException as e:
                self.console.print(f"[red]✗[/red] Error en página {page + 1}: {str(e)}")
                raise Exception(f"Error en la solicitud HTTP: {str(e)}")

        return final_results

    def custom_results(self, results):
        """
        Procesa y filtra los resultados brutos.

        Args:
            results (list): Lista de resultados raw de la API

        Returns:
            list: Lista de resultados procesados
        """
        return [
            {
                "title": result.get("title"),
                "description": result.get("snippet"),
                "link": result.get("link"),
            }
            for result in results
        ]

    def extract_potential_keys(self, text):
        """
        Busca posibles claves API en un texto usando expresiones regulares.

        Args:
            text (str): Texto donde buscar las claves

        Returns:
            list: Lista de posibles claves encontradas
        """
        pattern = r'sk-[a-zA-Z0-9]{32,}'
        return re.findall(pattern, text)

    def display_results(self, query, site=None, start_page=1, pages=1, lang="lang_en", format_output=None):
        """
        Ejecuta la búsqueda y procesa los resultados según el formato especificado.
        """
        results = self.search(query, site, start_page, pages, lang)

        if not format_output:
            format_output = ['console']

        from results import ResultsProcessor
        processor = ResultsProcessor(results, query)

        if 'console' in format_output:
            processor.display_console()
        if 'json' in format_output:
            processor.save_json()
        if 'html' in format_output:
            processor.save_html()

        # Guardar claves encontradas
        potential_keys = []
        for result in results:
            keys = self.extract_potential_keys(result['description'] + result['title'])
            potential_keys.extend(keys)

        self.save_keys(potential_keys)

        # Devolver el procesador para el análisis LLM
        return processor

    def save_keys(self, keys):
        """
        Guarda las claves encontradas en un archivo de texto.

        Args:
            keys (list): Lista de claves a guardar
        """
        if keys:
            try:
                with open("found_keys.txt", "w") as file:
                    for key in keys:
                        file.write(f"{key}\n")
                self.console.print("[green]✓[/green] Claves guardadas en 'found_keys.txt'")
                self.console.print(f"\n[green]Total de claves encontradas:[/green] {len(keys)}")
            except Exception as e:
                self.console.print(f"[red]Error guardando claves: {str(e)}[/red]")
        else:
            self.console.print("[yellow]No hay claves para guardar[/yellow]")