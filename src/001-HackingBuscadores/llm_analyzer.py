from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from datetime import datetime
from openai import OpenAI
from gpt4all import GPT4All
import os
from dotenv import load_dotenv


class IAGeneratorInterface:
    """Define la interfaz común para los generadores de IA."""

    def generate(self, prompt):
        """Genera una salida basada en un mensaje de entrada."""
        raise NotImplementedError("Este método debe ser implementado por la subclase.")


class OpenAIGenerator(IAGeneratorInterface):
    """Implementación de OpenAI."""

    def __init__(self, model_name='gpt-4o-mini'):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model_name = model_name

    def generate(self, prompt):
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model_name,
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content


class GPT4AllGenerator(IAGeneratorInterface):
    """Implementación de GPT4All para generación local."""

    def __init__(self, model_name="orca-mini-3b-gguf2-q4_0.gguf"):
        self.model = GPT4All(model_name)

    def generate(self, prompt):
        return self.model.generate(prompt)


class LLMAnalyzer:
    """Clase principal para el análisis usando modelos de lenguaje."""

    def __init__(self, results=None, query=None, generator=None):
        self.console = Console()
        self.results = results
        self.query = query
        self.generator = generator or OpenAIGenerator()

    def analyze_results(self, results, query):
        """Analiza los resultados usando el generador configurado."""
        try:
            self.console.print("\n[cyan]Preparando análisis...[/cyan]")
            self.console.print(f"[yellow]Total resultados:[/yellow] {len(results)}")

            prompt = self._prepare_analysis_prompt(results, query)
            content = self.generator.generate(prompt)
            self._display_analysis(content)

        except Exception as e:
            self.console.print(f"[red]Error durante el análisis: {str(e)}[/red]")

    def generate_dork(self, description):
        """Genera un Google Dork basado en una descripción."""
        try:
            self.console.print("\n[cyan]Generando Google Dork...[/cyan]")

            prompt = self._build_dork_prompt(description)
            dork = self.generator.generate(prompt)

            self.console.print(Panel.fit(
                f"[cyan]Descripción:[/cyan] {description}\n\n"
                f"[green]Google Dork:[/green] {dork}",
                title="[bold]Google Dork Generado[/bold]",
                border_style="cyan"
            ))

            return dork
        except Exception as e:
            self.console.print(f"[red]Error generando el dork: {str(e)}[/red]")
            return None

    def _prepare_analysis_prompt(self, results, query):
        results_text = "\n\n".join([
            f"Resultado #{i + 1}:\n"
            f"- Título: {r['title']}\n"
            f"- Descripción: {r['description']}\n"
            f"- URL: {r['link']}"
            for i, r in enumerate(results[:5])
        ])

        return f"""
Por favor, analiza los siguientes resultados de una búsqueda de Google Dorking:

CONSULTA UTILIZADA:
{query}

RESULTADOS PRINCIPALES:
{results_text}

Por favor, proporciona un análisis estructurado que incluya:

1. RESUMEN GENERAL:
   - Descripción general de los hallazgos
   - Patrones identificados
   - Nivel de sensibilidad de la información encontrada

2. RIESGOS DE SEGURIDAD:
   - Riesgos específicos identificados
   - Potencial impacto
   - Severidad de cada riesgo

3. RECOMENDACIONES:
   - Acciones inmediatas recomendadas
   - Medidas preventivas
   - Mejores prácticas sugeridas

4. OBSERVACIONES ADICIONALES:
   - Cualquier aspecto notable o inusual
   - Contexto adicional relevante

Por favor, usa formato Markdown en tu respuesta para mejorar la legibilidad.
"""

    def _build_dork_prompt(self, description):
        return f"""
Genera un Google Dork específico basado en la descripción del usuario. Un Google Dork utiliza operadores avanzados en motores de búsqueda para encontrar información específica que es difícil de encontrar mediante una búsqueda normal.

Ejemplos de referencia:

Descripción: Documentos PDF relacionados con la seguridad informática publicados en el último año.
Google Dork: filetype:pdf "seguridad informática" after:2023-01-01

Descripción: Presentaciones de Powerpoint sobre cambio climático disponibles en sitios .edu.
Google Dork: site:.edu filetype:ppt "cambio climático"

Ahora, genera un Google Dork preciso para esta descripción:
{description}

Responde SOLO con el Google Dork generado, sin explicaciones adicionales.
"""

    def _display_analysis(self, analysis):
        """Muestra y guarda el análisis."""
        self.console.print("\n")
        self.console.print(Panel.fit(
            Markdown(analysis),
            title="[cyan]Análisis de Seguridad[/cyan]",
            border_style="cyan",
            padding=(1, 2),
            title_align="center"
        ))

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"security_analysis_{timestamp}.md"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"""# Análisis de Seguridad - Google Dorking

## Metadatos
- **Fecha**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Consulta**: {self.query}
- **Total de resultados analizados**: {len(self.results) if self.results else 0}
- **Modelo utilizado**: {self.generator.__class__.__name__}

## Análisis Detallado
{analysis}

---
*Generado automáticamente por Ninja Dorks - Herramienta de Google Dorking*
""")
            self.console.print(f"[green]✓[/green] Análisis guardado en: {filename}")
        except Exception as e:
            self.console.print(f"[red]Error guardando el análisis: {str(e)}[/red]")