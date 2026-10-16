# Biblioteca LaCuerda

Herramienta escrita en Python para descargar y organizar localmente acordes, tablaturas y otras transcripciones de canciones publicadas en [acordes.lacuerda.net](https://acordes.lacuerda.net/).

El programa utiliza un archivo HTML local (`lista.html`) con el listado de canciones de un artista. A partir de ese listado, identifica las canciones y sus versiones, descarga el contenido disponible y guarda cada transcripción como un archivo de texto `.txt`.

## Características

- **Menú interactivo** para iniciar una descarga, verificar el listado o consultar el estado de un artista.
- **Lectura de `lista.html` local**, sin tener que reconstruir el listado desde cero en cada ejecución.
- **Detección automática del artista** cuando el HTML contiene la variable `bName`.
- **Resolución de rutas de artistas**: prueba nombres de URL habituales y permite ingresar manualmente la ruta correcta si es necesario.
- **Soporte para varias versiones** de una canción y distintos tipos de transcripción:
  - Acordes
  - Tablatura
  - Bajo
  - Armónica
  - Teclado
- **Prevención de duplicados**: omite archivos `.txt` que ya existen.
- **Reintento de errores transitorios** de conexión y tiempo de espera.
- **Escritura segura de archivos** mediante archivos temporales antes de guardar la versión definitiva.
- **Interrupción controlada**: al presionar `Ctrl+C`, intenta terminar el elemento en curso y cerrar de forma ordenada. Al volver a ejecutar el programa, las descargas existentes se omiten.
- **Consulta del estado de un artista**, contando los archivos `.txt` guardados en su carpeta.

## Requisitos

- Python 3.9 o superior recomendado.
- Conexión a Internet.
- Un archivo `lista.html` válido, obtenido previamente de LaCuerda y ubicado en la carpeta desde la que se ejecuta el programa.

## Instalación

### 1. Clonar el repositorio

```bash
git clone URL_DE_TU_REPOSITORIO
cd NOMBRE_DEL_REPOSITORIO
```

Reemplazá `URL_DE_TU_REPOSITORIO` y `NOMBRE_DEL_REPOSITORIO` por los datos de tu repositorio de GitHub.

### 2. Instalar las dependencias

El proyecto utiliza `requests` y `beautifulsoup4`.

```bash
python -m pip install requests beautifulsoup4
```

### 3. Preparar los archivos

Colocá en una misma carpeta:

```text
.
├── lacuerda.py
├── funciones.py
└── lista.html
```

**Importante:** `lacuerda.py` contiene `import funciones as flc`. Por eso, el módulo auxiliar debe llamarse exactamente `funciones.py` y estar en la misma carpeta que el lanzador. Si el archivo descargado se llama `funciones.py`, renombralo a `funciones.py` antes de ejecutar el programa.

`lista.html` debe corresponder al listado de canciones que querés procesar. El programa no descarga automáticamente el índice del artista: lee el archivo local.

## Uso

Desde la terminal, dentro de la carpeta del proyecto, ejecutá:

```bash
python lacuerda.py
```

Se mostrará el menú principal:

```text
========== Biblioteca LaCuerda ===========
  1) Descargar / actualizar biblioteca (usa el lista.html actual)
  2) Verificar el lista.html actual (sin descargar nada)
  3) Ver estado de descargas de un artista
  4) Salir
==========================================
```

### Opción 1: Descargar / actualizar biblioteca

Procesa el `lista.html` actual y descarga las versiones disponibles de las canciones que todavía no estén guardadas.

El programa intenta detectar el nombre del artista a partir del HTML. Si no puede encontrarlo, lo solicita por consola. Después valida la ruta del artista en el sitio; si las rutas generadas automáticamente no funcionan, permite ingresar manualmente el tramo correspondiente de la URL.

Los archivos se guardan dentro de `Biblioteca_LaCuerda`, en una carpeta por artista.

### Opción 2: Verificar `lista.html`

Realiza comprobaciones sin descargar canciones. Informa el artista detectado, la cantidad de canciones únicas, la carpeta de destino y los archivos que ya existen. También prueba las posibles rutas del artista en el sitio.

Usá esta opción antes de una descarga si querés comprobar que el listado local y la ruta del artista parecen correctos.

### Opción 3: Ver estado de descargas

Solicita el nombre del artista tal como se guardó en la carpeta y muestra la ruta de destino y la cantidad de archivos `.txt` encontrados.

### Opción 4: Salir

Cierra el programa.

## Estructura de salida

La biblioteca se crea automáticamente cuando se inicia una descarga. La estructura general es similar a esta:

```text
Biblioteca_LaCuerda/
└── Nombre_Del_Artista/
    ├── Cancion Uno - Acordes.txt
    ├── Cancion Uno - Tablatura.txt
    ├── Cancion Dos - Acordes.txt
    └── ...
```

Los nombres concretos dependen del título de la canción y del tipo o número de versión detectado.

Cada archivo de texto incluye los metadatos de la descarga y el contenido extraído:

```text
ARTISTA: Nombre del artista
CANCION: Título de la canción
VERSION: Acordes
URL: https://acordes.lacuerda.net/...

========================================

[Contenido de la transcripción]
```

Si una canción tiene varias versiones del mismo tipo, se agregan etiquetas numeradas para evitar que los archivos se sobrescriban.

## Errores, reintentos y continuidad

- Los tiempos de espera y ciertos errores de conexión se ponen en una cola para volver a intentarlos al final del recorrido.
- Si el servidor devuelve un error HTTP, el programa informa el problema con un mensaje breve.
- Si la ruta del artista parece incorrecta y se detecta un `404` en el primer intento real de descarga, se solicita una ruta manual y se reinicia el recorrido.
- Los archivos se escriben primero en un archivo temporal y luego se renombran, para reducir el riesgo de dejar una descarga incompleta con el nombre definitivo.
- Si detenés el proceso con `Ctrl+C`, podés volver a ejecutarlo. Los archivos ya existentes se omiten automáticamente.

La continuidad se basa en los archivos `.txt` ya guardados: el programa no necesita una base de datos adicional para reconocerlos.

## Archivos del proyecto

- **`lacuerda.py`**: punto de entrada; muestra el menú y llama a las funciones correspondientes.
- **`funciones.py`**: contiene la lógica de lectura de `lista.html`, análisis de canciones, resolución de rutas, descarga y guardado de archivos.
- **`lista.html`**: listado local de canciones que se va a procesar. Debe prepararse por separado.

## Consideraciones

- El contenido disponible depende de LaCuerda y de la validez de las páginas enlazadas desde el listado.
- El programa espera encontrar la estructura HTML de las transcripciones en el sitio. Si LaCuerda cambia su estructura, puede ser necesario adaptar el extractor.
- Se aplica una pausa entre solicitudes y se limita el tiempo de espera de las conexiones; aun así, las descargas pueden tardar según la cantidad de canciones y la respuesta del servidor.
- Usá la herramienta de manera responsable, respetando las condiciones del sitio y los derechos de los autores y titulares de las transcripciones.

## Solución de problemas

**No encuentra `lista.html`**

Comprobá que el archivo esté en el directorio actual desde el que ejecutás el programa y que su nombre sea exactamente `lista.html`.

**Aparece `ModuleNotFoundError: No module named 'funciones'`**

Verificá que el archivo auxiliar se llame `funciones.py` y esté junto a `lacuerda.py`.

**No detecta al artista**

El programa puede solicitar el nombre por consola si no encuentra `bName` en el HTML. Ingresá el nombre con el que querés identificar la carpeta.

**La ruta del artista devuelve `404`**

Cuando se solicite, ingresá el tramo correcto de la URL del artista, es decir, la parte que aparece entre `acordes.lacuerda.net/` y la siguiente barra.

**Faltan algunas versiones**

Algunas páginas pueden no estar disponibles o no contener el bloque de transcripción esperado. Revisá los mensajes de la consola y volvé a ejecutar el programa si hubo fallos transitorios.

---

**Proyecto personal de automatización y organización local de transcripciones musicales.**
