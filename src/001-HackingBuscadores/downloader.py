import os
import requests
from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, DownloadColumn, TimeRemainingColumn
from urllib.parse import urlparse, unquote


class FileDownloader:
    """Clase para descargar archivos desde URLs encontradas en los resultados."""

    def __init__(self, directorio_destino="downloads"):
        """
        Inicializa el FileDownloader con un directorio de destino.

        Args:
            directorio_destino (str): Ruta del directorio para los archivos descargados
        """
        self.directorio = directorio_destino
        self.console = Console()
        self._crear_directorio()

    def _crear_directorio(self):
        """Crea el directorio de destino si no existe."""
        if not os.path.exists(self.directorio):
            os.makedirs(self.directorio)
            self.console.print(f"[green]✓[/green] Directorio creado: {self.directorio}")

    def _obtener_nombre_archivo(self, url, headers=None):
        """
        Obtiene un nombre de archivo apropiado de la URL o headers.

        Args:
            url (str): URL del archivo
            headers (dict): Headers de la respuesta HTTP

        Returns:
            str: Nombre del archivo
        """
        # Intentar obtener el nombre del Content-Disposition
        if headers and 'content-disposition' in headers:
            import re
            matches = re.findall('filename=(.+)', headers['content-disposition'])
            if matches:
                return matches[0].strip('"')

        # Obtener el nombre de la URL
        parsed_url = urlparse(url)
        nombre_archivo = unquote(os.path.basename(parsed_url.path))

        # Si no hay nombre en la URL, usar el último segmento del path
        if not nombre_archivo:
            nombre_archivo = unquote(parsed_url.path.split('/')[-1])

        # Si aún no hay nombre, usar el hostname con timestamp
        if not nombre_archivo:
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nombre_archivo = f"{parsed_url.hostname}_{timestamp}"

        return nombre_archivo

    def descargar_archivo(self, url):
        """
        Descarga un archivo desde una URL con barra de progreso.

        Args:
            url (str): URL del archivo a descargar
        """
        try:
            # Realizar solicitud HEAD primero para obtener el tamaño
            head_response = requests.head(url, allow_redirects=True)
            total_size = int(head_response.headers.get('content-length', 0))

            # Obtener nombre del archivo
            nombre_archivo = self._obtener_nombre_archivo(url, head_response.headers)
            ruta_completa = os.path.join(self.directorio, nombre_archivo)

            # Configurar la barra de progreso
            with Progress(
                    TextColumn("[bold blue]{task.description}"),
                    BarColumn(bar_width=50),
                    "[progress.percentage]{task.percentage:>3.0f}%",
                    DownloadColumn(),
                    TimeRemainingColumn(),
            ) as progress:

                # Crear la tarea de descarga
                task = progress.add_task(f"Descargando {nombre_archivo}", total=total_size)

                # Realizar la descarga con streaming
                response = requests.get(url, stream=True)
                with open(ruta_completa, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                            progress.update(task, advance=len(chunk))

            self.console.print(f"[green]✓[/green] Archivo descargado: {ruta_completa}")
            return True

        except Exception as e:
            self.console.print(f"[red]✗[/red] Error al descargar {url}: {str(e)}")
            return False

    def filtrar_descargar_archivos(self, urls, tipos_archivos=None):
        """
        Filtra y descarga archivos según sus extensiones.

        Args:
            urls (list): Lista de URLs a descargar
            tipos_archivos (list, optional): Lista de extensiones permitidas
        """
        if not urls:
            self.console.print("[yellow]No hay URLs para descargar[/yellow]")
            return

        if tipos_archivos is None:
            tipos_archivos = ["all"]

        self.console.print(f"\n[bold cyan]Iniciando descarga de archivos[/bold cyan]")
        self.console.print(f"Tipos de archivo permitidos: {', '.join(tipos_archivos)}\n")

        descargas_exitosas = 0
        for url in urls:
            if tipos_archivos == ["all"] or any(url.lower().endswith(f".{tipo.lower()}") for tipo in tipos_archivos):
                if self.descargar_archivo(url):
                    descargas_exitosas += 1

        self.console.print(f"\n[green]Descargas completadas:[/green] {descargas_exitosas}/{len(urls)}")