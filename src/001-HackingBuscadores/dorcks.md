# Comandos Principales para Google Hacking

Estos comandos permiten realizar búsquedas avanzadas y específicas en Google para encontrar información más precisa o detalles particulares en páginas web. Se utiliza un formato estructurado donde el comando va seguido directamente de la consulta sin espacios.

---

## **Comandos Principales**

### `define:término`
- **Descripción**: Devuelve definiciones del término desde distintas páginas web.
- **Ejemplo**: `define:inteligencia artificial`  
  - Resultado: Muestra definiciones de "inteligencia artificial".

---

### `filetype:término`
- **Descripción**: Busca páginas o documentos con la extensión de archivo especificada (como PDF, DOCX, SQL, etc.).
- **Nota**: El comando `ext:término` es equivalente.
- **Ejemplo**: `filetype:pdf hacking`  
  - Resultado: Devuelve documentos PDF relacionados con "hacking".

---

### `site:sitio/dominio`
- **Descripción**: Restringe la búsqueda a un sitio web o dominio específico.
- **Ejemplo**: `site:example.com password`  
  - Resultado: Busca "password" exclusivamente dentro del dominio `example.com`.

---

### `link:url`
- **Descripción**: Encuentra páginas que enlacen a la URL especificada.
- **Nota**: Solo muestra páginas con un PageRank de 5 o superior.
- **Ejemplo**: `link:github.com`  
  - Resultado: Muestra páginas que contienen enlaces hacia GitHub.

---

### `cache:url`
- **Descripción**: Muestra la copia en caché de la página almacenada por Google.
- **Ejemplo**: `cache:example.com`  
  - Resultado: Abre la versión almacenada más reciente del sitio.

---

### `info:url`
- **Descripción**: Presenta información sobre la página correspondiente a la URL.
- **Ejemplo**: `info:example.com`  
  - Resultado: Muestra detalles sobre el sitio `example.com`.

---

### `related:url`
- **Descripción**: Encuentra páginas similares a la URL especificada.
- **Ejemplo**: `related:example.com`  
  - Resultado: Sitios web similares al especificado.

---

### `allinanchor:términos`
- **Descripción**: Busca páginas cuyos enlaces contengan los términos en su texto.
- **Ejemplo**: `allinanchor:seguridad hacking`  
  - Resultado: Devuelve páginas enlazadas con "seguridad" y "hacking".

---

### `inanchor:término`
- **Descripción**: Busca páginas enlazadas con un texto específico en los enlaces.
- **Ejemplo**: `inanchor:seguridad`  
  - Resultado: Resultados enlazados con "seguridad" en el texto del enlace.

---

### `allintext:términos` / `intext:término`
- **`allintext`**: Restringe los resultados a aquellos que contienen todos los términos en el texto.
- **`intext`**: Busca páginas que contengan un término específico en el texto.
- **Ejemplo**: 
  - `allintext:contraseñas robadas`  
    - Páginas con ambos términos.
  - `intext:contraseña`  
    - Páginas con el término "contraseña".

---

### `allinurl:términos` / `inurl:término`
- **`allinurl`**: Busca resultados donde todos los términos están en la URL.
- **`inurl`**: Busca resultados donde un término específico está en la URL.
- **Ejemplo**: 
  - `allinurl:login password`  
    - URLs que contienen ambos términos.
  - `inurl:admin`  
    - URLs que contienen "admin".

---

### `allintitle:términos` / `intitle:término`
- **`allintitle`**: Restringe los resultados a títulos que contengan todos los términos.
- **`intitle`**: Busca títulos que contengan un término específico.
- **Ejemplo**: 
  - `allintitle:servidor error`  
    - Resultados con ambos términos en el título.
  - `intitle:servidor`  
    - Títulos con el término "servidor".

---

## **Operadores Booleanos**

Los operadores booleanos son símbolos y palabras clave que combinan o modifican las búsquedas para obtener resultados más precisos.

### `"palabras exactas"`
- **Descripción**: Busca la frase exacta entre comillas.
- **Ejemplo**: `"error de servidor 404"`  
  - Resultado: Devuelve resultados con esa frase exacta.

---

### `-palabra`
- **Descripción**: Excluye la palabra de los resultados.
- **Ejemplo**: `gmail -hotmail`  
  - Resultado: Muestra resultados con "gmail" pero excluye "hotmail".

---

### `OR` / `|`
- **Descripción**: Busca resultados que contengan uno u otro término.
- **Ejemplo**: `seguridad OR hacking`  
  - Resultado: Muestra resultados relacionados con "seguridad" o "hacking".

---

### `+palabra`
- **Descripción**: Obliga a incluir palabras que Google usualmente ignora (como preposiciones, acentos, etc.).
- **Ejemplo**: `+cómo programar`  
  - Resultado: Asegura que "cómo" se incluya en los resultados.

---

### `*`
- **Descripción**: Actúa como comodín para sustituir palabras.
- **Ejemplo**: `"ataque * hacker"`  
  - Resultado: Encuentra frases como "ataque cibernético hacker" o "ataque avanzado hacker".

---

## **Ejemplo Completo de Google Dorks**

### **Buscar ficheros SQL que contengan contraseñas**
- **Dork**: `filetype:sql "MySQL dump" (pass|password|passwd|pwd)`  
- **Resultado esperado**:  
  Devuelve archivos SQL con referencias a "MySQL dump" y términos relacionados con contraseñas.

---

### **Buscar páginas relacionadas con administración**
- **Dork**: `inurl:admin intitle:login`  
- **Resultado esperado**:  
  Devuelve páginas de inicio de sesión con "admin" en la URL y "login" en el título.

---

Con estos comandos y operadores, puedes realizar búsquedas específicas y optimizadas en Google para encontrar la información deseada.