# Ninja Dorks - Google Dorking Tool

Ninja Dorks es una herramienta de Google Dorking diseñada para realizar búsquedas avanzadas y personalizadas, integrando múltiples opciones como el uso de Selenium, la API de Google, análisis con modelos de lenguaje (LLMs) y exportación de resultados en formatos estructurados. La herramienta está diseñada para profesionales de ciberseguridad, investigadores y usuarios interesados en búsquedas avanzadas utilizando operadores de Google.

## Características

- **Búsqueda con Selenium:** Realiza búsquedas dinámicas simulando un navegador real para extraer resultados avanzados.
- **Integración con la API de Google:** Una alternativa eficiente para búsquedas estructuradas sin necesidad de Selenium.
- **Soporte de operadores de Google Dorking:** Utiliza operadores avanzados como `site:`, `filetype:`, `inurl:` y más para búsquedas específicas.
- **Análisis con Modelos de Lenguaje:** Analiza resultados utilizando OpenAI o GPT4All para identificar patrones y generar resúmenes.
- **Exportación de Resultados:** Guarda resultados en formatos JSON y HTML para mayor accesibilidad y análisis posterior.
- **Descarga de Archivos:** Descarga documentos encontrados en las búsquedas según extensiones específicas como `pdf`, `txt`, o `doc`.

## Requisitos

1. **Python 3.8 o superior**
2. **Bibliotecas necesarias:**
   - Selenium
   - Webdriver Manager
   - Rich
   - Requests
   - OpenAI (opcional)
   - GPT4All (opcional)

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tu-repo/ninja-dorks.git
   cd ninja-dorks
    ```

2. Configuracion entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate # En Windows: .venv\Scripts\activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

4. Configura las claves de la API de Google:

Crea un archivo .env en el directorio raíz del proyecto.
Añade las siguientes variables:
    
    ```bash
    GOOGLE_API_KEY=your_api_key
    GOOGLE_ENGINE_ID=your_engine_id
    ```

Uso

```bash
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
```

5. Recomendaciones

Recomendaciones
Usa esta herramienta de manera ética y respetando las leyes locales.
Limita las búsquedas a datos accesibles públicamente y dominios que no estén restringidos.
Introduce tiempos de espera en búsquedas repetitivas para evitar bloqueos de Google.

## Licencia

Ninja Dorks es un software de código abierto bajo la licencia MIT. Consulta el archivo LICENSE para más información.

## Contacto

- LinkedIn: [linkedin.com/in/adrianinfantes](https://www.linkedin.com/in/adrianinfantes)
- Mail: [infantesromeroadrian@gmail.com](mailto:infantesromeroadrian@gmail.com)