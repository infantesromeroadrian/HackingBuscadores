
import json
from rich.console import Console
from rich.table import Table
from datetime import datetime

class ResultsProcessor:
    """Clase para procesar y mostrar resultados de Google Dorking en diferentes formatos."""

    def __init__(self, results, query):
        """
        Inicializa el procesador de resultados.

        Args:
            results (list): Lista de resultados de la búsqueda
            query (str): Consulta utilizada para la búsqueda
        """
        self.results = results if results else []
        self.query = query
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.console = Console()

    def display_console(self):
        """Muestra los resultados en la consola con un formato atractivo."""
        self.console.print("\n[bold cyan]🔍 Google Dorking Results[/bold cyan]")
        self.console.print(f"[yellow]Query:[/yellow] {self.query}")
        self.console.print(f"[yellow]Timestamp:[/yellow] {self.timestamp}\n")

        if not self.results:
            self.console.print("[yellow]No se encontraron resultados[/yellow]")
            return

        table = Table(show_header=True, header_style="bold magenta", box=None)
        table.add_column("№", style="cyan", justify="right")
        table.add_column("Title", style="bright_white", width=50)
        table.add_column("Description", style="white", width=60)
        table.add_column("URL", style="blue")

        for i, result in enumerate(self.results, 1):
            title = str(result.get('title', ''))[:47] + "..." if len(str(result.get('title', ''))) > 50 else str(
                result.get('title', ''))
            desc = str(result.get('description', ''))[:57] + "..." if len(
                str(result.get('description', ''))) > 60 else str(result.get('description', ''))
            url = str(result.get('link', ''))[:77] + "..." if len(str(result.get('link', ''))) > 80 else str(
                result.get('link', ''))

            table.add_row(
                str(i),
                title,
                desc,
                url
            )

        self.console.print(table)
        self.console.print(f"\n[green]Total resultados encontrados:[/green] {len(self.results)}")

    def save_json(self):
        """Guarda los resultados en formato JSON."""
        output = {
            "query": self.query,
            "timestamp": self.timestamp,
            "total_results": len(self.results),
            "results": self.results
        }

        filename = f"dorking_results_{self.timestamp}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=4)
            self.console.print(f"\n[green]✓[/green] Resultados guardados en JSON: {filename}")
        except Exception as e:
            self.console.print(f"[red]Error guardando JSON: {str(e)}[/red]")

    def save_html(self):
        """Guarda los resultados en formato HTML."""
        filename = f"dorking_results_{self.timestamp}.html"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("<html><head><title>Google Dorking Results</title></head><body>\n")
                f.write(f"<h1>Resultados de Google Dorking</h1>\n")
                f.write(f"<h2>Query: {self.query}</h2>\n")
                f.write(f"<h3>Timestamp: {self.timestamp}</h3>\n")
                f.write("<table border='1' style='border-collapse: collapse; width: 100%;'>\n")
                f.write("<tr><th>#</th><th>Title</th><th>Description</th><th>URL</th></tr>\n")

                for i, result in enumerate(self.results, 1):
                    title = result.get('title', 'N/A')
                    description = result.get('description', 'N/A')
                    url = result.get('link', 'N/A')
                    f.write(f"<tr><td>{i}</td><td>{title}</td><td>{description}</td><td><a href='{url}'>{url}</a></td></tr>\n")

                f.write("</table>\n")
                f.write("</body></html>\n")

            self.console.print(f"[green]✓[/green] Resultados guardados en HTML: {filename}")
        except Exception as e:
            self.console.print(f"[red]Error guardando HTML: {str(e)}[/red]")
