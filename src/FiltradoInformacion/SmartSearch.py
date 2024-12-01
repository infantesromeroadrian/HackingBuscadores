

#!/usr/bin/env python3
"""
SmartSearch - Herramienta avanzada de búsqueda en archivos usando expresiones regulares o IA.

Esta herramienta permite realizar búsquedas complejas en archivos de texto utilizando:
- Expresiones regulares
- Modelos de inteligencia artificial (OpenAI GPT)

Características principales:
- Búsqueda recursiva en directorios
- Filtrado de comentarios y ejemplos de código
- Visualización con contexto y colores
- Soporte para diferentes tipos de archivo
- Exclusión de directorios y archivos
- Búsqueda contextual con IA y estimación de costes

Uso básico:
    python smartsearch.py directorio -p "patrón"

Ejemplos:
    # Buscar 'password' en archivos Python
    python smartsearch.py . -p "password" --ext .py

    # Buscar con IA en archivos Markdown
    python smartsearch.py . --prompt "Describe el contenido de este archivo" --ext .md
"""

import os
import re
import argparse
from typing import Dict, List, Set
from datetime import datetime
from rich.console import Console
from rich.progress import track
from rich.panel import Panel
from dotenv import load_dotenv
import openai


class IAMatcher:
    """
    Manejo de búsqueda mediante inteligencia artificial usando modelos de OpenAI.
    """

    def __init__(self, model_name="gpt-3.5-turbo", max_tokens=100):
        """
        Inicializa el buscador IA.

        Args:
            model_name (str): Modelo de OpenAI a utilizar.
            max_tokens (int): Número máximo de tokens de salida.
        """
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.console = Console()

        # Precios de los modelos
        self.prices = {
            "gpt-4": {"input_cost": 0.03, "output_cost": 0.06},
            "gpt-3.5-turbo": {"input_cost": 0.0005, "output_cost": 0.0015},
        }

    def calculate_cost(self, prompt_length, text_length):
        """
        Calcula el coste estimado de usar un modelo de IA.

        Args:
            prompt_length (int): Longitud del prompt en tokens.
            text_length (int): Longitud del texto en tokens.

        Returns:
            tuple: Total de tokens y coste estimado en dólares.
        """
        total_tokens = prompt_length + text_length
        input_cost = (total_tokens / 1000) * self.prices[self.model_name]["input_cost"]
        output_cost = (self.max_tokens / 1000) * self.prices[self.model_name]["output_cost"]
        return total_tokens, input_cost + output_cost

    def split_text(self, text, max_context_size):
        """
        Divide el texto en segmentos adecuados al modelo seleccionado.

        Args:
            text (str): Texto a dividir.
            max_context_size (int): Tamaño máximo del contexto del modelo.

        Returns:
            list: Lista de segmentos del texto.
        """
        return [text[i:i + max_context_size] for i in range(0, len(text), max_context_size)]

    def find_with_ai(self, text, prompt):
        """
        Encuentra información utilizando un modelo de IA.

        Args:
            text (str): Texto en el que se realizará la búsqueda.
            prompt (str): Instrucción para el modelo.

        Returns:
            list: Respuestas generadas por el modelo.
        """
        context_window_size = 4096 if self.model_name == "gpt-3.5-turbo" else 8192
        segments = self.split_text(text, context_window_size)
        results = []

        for index, segment in enumerate(segments):
            self.console.print(f"Procesando segmento {index + 1}/{len(segments)}...")
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[{"role": "user", "content": f"{prompt}\n\n{segment}"}],
                max_tokens=self.max_tokens,
            )
            results.append(response.choices[0].message["content"])

        return results


class SmartSearch:
    """
    Clase principal para realizar búsquedas inteligentes en archivos mediante expresiones regulares o IA.
    """

    def __init__(self, dir_path: str, ignore_patterns: Set[str] = None,
                 file_extensions: List[str] = None, ia_model="gpt-3.5-turbo", max_tokens=100):
        self.dir_path = os.path.abspath(dir_path)
        self.ignore_patterns = ignore_patterns or {'.git', '__pycache__', '.env'}
        self.file_extensions = file_extensions
        self.console = Console()
        self.ia_matcher = IAMatcher(model_name=ia_model, max_tokens=max_tokens)

    def search_with_ai(self, prompt):
        """
        Realiza una búsqueda en los archivos usando IA.

        Args:
            prompt (str): Instrucción para el modelo.

        Returns:
            dict: Resultados por archivo.
        """
        results = {}
        files = self._get_files(True)

        for file_path in track(files, description="Procesando archivos con IA..."):
            content = self._read_file(file_path)
            if not content:
                continue

            prompt_length = len(prompt.split())
            text_length = len(content.split())
            total_tokens, cost = self.ia_matcher.calculate_cost(prompt_length, text_length)
            self.console.print(f"Procesando {file_path} ({total_tokens} tokens, aprox. ${cost:.4f})")

            responses = self.ia_matcher.find_with_ai(content, prompt)
            results[file_path] = responses

        return results

    def _get_files(self, recursive: bool) -> List[str]:
        """
        Obtiene la lista de archivos a procesar.

        Args:
            recursive (bool): Si debe buscar en subdirectorios.

        Returns:
            List[str]: Lista de rutas de archivos.
        """
        files = []
        for root, dirs, filenames in os.walk(self.dir_path):
            dirs[:] = [d for d in dirs if d not in self.ignore_patterns]
            for filename in filenames:
                file_path = os.path.join(root, filename)
                if self.file_extensions:
                    if not any(file_path.endswith(ext) for ext in self.file_extensions):
                        continue
                files.append(file_path)
        return files

    def _read_file(self, file_path: str) -> str:
        """
        Lee el contenido de un archivo.

        Args:
            file_path (str): Ruta del archivo.

        Returns:
            str: Contenido del archivo.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            self.console.print(f"[red]Error leyendo {file_path}: {e}[/red]")
            return ""


def main():
    """Función principal del programa."""
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Herramienta avanzada de búsqueda en archivos con regex o IA.",
    )
    parser.add_argument("directory", help="Directorio donde realizar la búsqueda")
    parser.add_argument("-p", "--pattern", help="Patrón regex para buscar")
    parser.add_argument("--prompt", help="Prompt para búsqueda con IA")
    parser.add_argument("--model", default="gpt-3.5-turbo", help="Modelo de IA a utilizar")
    parser.add_argument("--max-tokens", type=int, default=100, help="Máximo de tokens generados por IA")
    parser.add_argument("--ext", help="Extensiones de archivo a procesar (separadas por comas)")

    args = parser.parse_args()
    file_extensions = args.ext.split(",") if args.ext else None

    searcher = SmartSearch(args.directory, file_extensions=file_extensions, ia_model=args.model, max_tokens=args.max_tokens)

    if args.prompt:
        results = searcher.search_with_ai(args.prompt)
        for file, responses in results.items():
            print(f"\nArchivo: {file}")
            for response in responses:
                print(f"\t- {response}")
    else:
        print("Debe proporcionar un patrón de regex (-p) o un prompt (--prompt).")


if __name__ == "__main__":
    main()
