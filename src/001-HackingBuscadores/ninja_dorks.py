import os
from dotenv import load_dotenv
from googledorking import GoogleDorking
from SeleniumModule import SeleniumSearcher
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from llm_analyzer import LLMAnalyzer, OpenAIGenerator, GPT4AllGenerator


def setup_argparse():
    """
    Configura los argumentos de línea de comandos para el script.

    Retorna un objeto argparse.ArgumentParser con todos los argumentos configurados.
    """
    parser = argparse.ArgumentParser(
        description="Herramienta de Google Dorking para búsquedas personalizadas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Ejemplos de uso:
        python ninja_dorks.py                                   # Búsqueda predeterminada
        python ninja_dorks.py -q "password" -s example.com      # Búsqueda específica en un sitio
        python ninja_dorks.py -f json html                     # Guardar resultados en JSON y HTML
        python ninja_dorks.py -p 5 -l lang_es                  # Buscar 5 páginas en español
        python ninja_dorks.py -d pdf txt                       # Descargar archivos PDF y TXT
        python ninja_dorks.py -q "filetype:pdf" -p 3 -d pdf    # Buscar y descargar PDFs
        python ninja_dorks.py --analyze                        # Analizar resultados con OpenAI
        python ninja_dorks.py -g "archivos PDF confidenciales" # Generar dork desde descripción
        python ninja_dorks.py --local-llm                      # Usar modelo local en vez de OpenAI
        python ninja_dorks.py --use-selenium -q "site:example.com admin" # Buscar usando Selenium
        """,
    )

    # Argumentos principales
    parser.add_argument(
        "-q",
        "--query",
        help="Consulta de búsqueda (si no se especifica, se usa la búsqueda por defecto)",
        default='site:github.com "sk-" "api_key"',
    )

    parser.add_argument(
        "-p", "--pages", type=int, help="Número de páginas a buscar", default=2
    )

    parser.add_argument(
        "-s", "--site", help="Sitio específico donde buscar (opcional)", default=None
    )

    parser.add_argument(
        "-l", "--lang", help="Idioma de búsqueda (default: lang_en)", default="lang_en"
    )

    parser.add_argument(
        "--start-page", type=int, help="Página inicial de búsqueda", default=1
    )

    # Formato de salida
    parser.add_argument(
        "-f",
        "--format",
        nargs="+",
        choices=["console", "json", "html"],
        default=["console"],
        help="Formato(s) de salida de resultados (puede especificar varios)",
    )

    # Descarga de archivos
    parser.add_argument(
        "-d",
        "--download",
        nargs="*",
        help="Descargar archivos encontrados (opcionalmente especificar extensiones, ej: -d pdf txt)",
    )

    # Uso de Selenium
    parser.add_argument(
        "--use-selenium",
        action="store_true",
        help="Usar Selenium en lugar de la API de Google para realizar la búsqueda",
    )

    # Generación de Dorks
    parser.add_argument(
        "-g",
        "--generate-dork",
        help="Genera un Google Dork basado en una descripción en lenguaje natural",
        type=str,
    )

    # Análisis con modelos de lenguaje
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Analizar resultados usando el modelo de lenguaje",
    )

    parser.add_argument(
        "--model",
        help="Modelo a utilizar (default: gpt-4o-mini)",
        default="gpt-3.5-turbo",
    )

    parser.add_argument(
        "--local-llm",
        action="store_true",
        help="Usar modelo local (GPT4All) en vez de OpenAI",
    )

    # Modo de depuración
    parser.add_argument(
        "--debug", action="store_true", help="Mostrar información de depuración"
    )

    return parser


def check_environment():
    """
    Verifica y valida las variables de entorno necesarias.

    Retorna las claves de API (`api_key`, `search_engine_id`) necesarias para la API de Google.
    """
    console = Console()

    # Cargar las variables de entorno
    load_dotenv()

    # Obtener las claves desde las variables de entorno
    api_key = os.getenv("GOOGLE_API_KEY")
    search_engine_id = os.getenv("SEARCH_ENGINE_ID")

    # Validar que las claves estén configuradas
    if not api_key or not search_engine_id:
        console.print(
            Panel.fit(
                "[red]Error: Las claves de API no están configuradas correctamente[/red]\n"
                + "Asegúrate de tener un archivo .env con:\n"
                + "GOOGLE_API_KEY=tu_api_key\n"
                + "SEARCH_ENGINE_ID=tu_search_engine_id",
                title="Error de Configuración",
            )
        )
        return None, None

    return api_key, search_engine_id


def display_banner():
    """Muestra el banner de la aplicación."""
    console = Console()
    banner = """
    ███╗   ██╗██╗███╗   ██╗     ██╗ █████╗     ██████╗  ██████╗ ██████╗ ██╗  ██╗███████╗
    ████╗  ██║██║████╗  ██║     ██║██╔══██╗    ██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝██╔════╝
    ██╔██╗ ██║██║██╔██╗ ██║     ██║███████║    ██║  ██║██║   ██║██████╔╝█████╔╝ ███████╗
    ██║╚██╗██║██║██║╚██╗██║██   ██║██╔══██║    ██║  ██║██║   ██║██╔══██╗██╔═██╗ ╚════██║
    ██║ ╚████║██║██║ ╚████║╚█████╔╝██║  ██║    ██████╔╝╚██████╔╝██║  ██║██║  ██╗███████║
    ╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝ ╚════╝ ╚═╝  ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
    """
    console.print(f"[cyan]{banner}[/cyan]")
    console.print(
        "[yellow]Herramienta de Google Dorking para búsquedas personalizadas[/yellow]"
    )
    console.print(
        "[yellow]Desarrollado con fines educativos - Úsalo con responsabilidad[/yellow]\n"
    )


def main():
    """Función principal del programa."""
    console = Console()
    display_banner()

    # Configurar argumentos
    parser = setup_argparse()
    args = parser.parse_args()

    # Verificar configuración de ambiente
    api_key, search_engine_id = check_environment()
    if not args.use_selenium and (not api_key or not search_engine_id):
        return

    try:
        results = []
        if args.use_selenium:
            # Realiza la búsqueda usando Selenium
            console.print(
                Panel.fit("[cyan]Usando Selenium para realizar la búsqueda...[/cyan]")
            )
            selenium_searcher = SeleniumSearcher()
            selenium_searcher.initialize_browser()
            results = selenium_searcher.perform_search(args.query)
        else:
            # Realiza la búsqueda usando la API de Google
            console.print(
                Panel.fit(
                    "[cyan]Usando la API de Google para realizar la búsqueda...[/cyan]"
                )
            )
            dorking = GoogleDorking(api_key=api_key, engine_id=search_engine_id)
            results = dorking.search(
                query=args.query,
                site=args.site,
                pages=args.pages,
                lang=args.lang,
                start_page=args.start_page,
            )

        # Procesar y mostrar resultados
        from results import ResultsProcessor

        processor = ResultsProcessor(results, args.query)

        if "console" in args.format:
            processor.display_console()
        if "json" in args.format:
            processor.save_json()
        if "html" in args.format:
            processor.save_html()

        if args.download:
            processor.download_files(args.download)

        if args.analyze:
            console.print("\n[cyan]Iniciando análisis con IA...[/cyan]")
            generator = (
                GPT4AllGenerator() if args.local_llm else OpenAIGenerator(args.model)
            )
            analyzer = LLMAnalyzer(
                results=results, query=args.query, generator=generator
            )
            analyzer.analyze_results(results, args.query)

    except Exception as e:
        console.print(f"[red]Error durante la ejecución: {e}[/red]")


if __name__ == "__main__":
    main()
