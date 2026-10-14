# Biblioteca LaCuerda

Herramienta escrita en Python para recorrer el índice alfabético de artistas de [LaCuerda.net](https://acordes.lacuerda.net), obtener sus canciones y descargar las distintas versiones disponibles de acordes, tablaturas y otros formatos a archivos `.txt`.

La versión **v5.2** permite trabajar por letra del índice. Esto divide el recorrido en unidades independientes y evita tener que volver a procesar todo el sitio cuando se quiera actualizar una parte de la biblioteca.

## Características

- **Scraping por letra:** el usuario selecciona una letra de la A a la Z.
- **Descubrimiento automático de páginas:** obtiene los offsets del índice alfabético (`index0.html`, `index100.html`, `index200.html`, etc.) desde la paginación del sitio.
- **Descubrimiento de artistas:** extrae nombre, URL y cantidad de canciones declaradas del listado `ul#i_main`.
- **Extracción de canciones:** entra a cada artista y procesa `ul#b_main`, incluyendo título, identificador, enlace y atributo `lcd`.
- **Descarga de múltiples versiones:** interpreta el atributo `lcd` para identificar acordes, tablaturas y otros tipos de transcripción.
- **Una carpeta por letra:** cada letra tiene su propio directorio, con archivos de control y carpetas de artistas.
- **Informes JSON y TXT:** registra artistas, canciones, páginas de índice, cantidades y errores.
- **Reutilización de conexión HTTP:** utiliza una única `requests.Session()` durante el recorrido de una letra, permitiendo reutilizar conexiones cuando el servidor lo admite.
- **Peticiones moderadas:** espera un segundo entre peticiones por defecto.
- **Reanudación:** conserva el control parcial al interrumpir el proceso y omite archivos `.txt` que ya existen.
- **Escritura atómica:** los archivos de control y las canciones se escriben primero en archivos temporales y luego se reemplazan, reduciendo el riesgo de dejar archivos incompletos.
- **Reintentos:** vuelve a intentar algunas descargas que fallan por problemas transitorios de conexión.
- **Menú interactivo:** permite ejecutar el scraping, verificar una letra y consultar su estado.

## Requisitos

- Python 3.9 o posterior recomendado.
- Conexión a Internet.
- Bibliotecas Python:
  - `requests`
  - `beautifulsoup4`

## Instalación

1. Instalar Python si todavía no está instalado.
2. Clonar el repositorio o descargar sus archivos.
3. Abrir una terminal en la carpeta del proyecto.
4. Instalar las dependencias:

   ```bash
   python -m pip install requests beautifulsoup4
   ```

## Archivos del proyecto

```text
.
├── lacuerda.py
├── funciones.py
├── README.md
├── LICENSE
└── Biblioteca_LaCuerda/
    ├── a/
    │   ├── artistas.json
    │   ├── artistas.txt
    │   ├── Artista 1/
    │   │   ├── Canción - Acordes.txt
    │   │   └── Canción - Tablatura.txt
    │   └── ...
    ├── b/
    │   ├── artistas.json
    │   ├── artistas.txt
    │   └── ...
    └── ...
```

`Biblioteca_LaCuerda/` se crea al ejecutar el programa. No es necesario crear manualmente las carpetas por letra.

## Uso

Ejecutar:

```bash
python lacuerda.py
```

El programa presenta el siguiente menú:

```text
Biblioteca LaCuerda v5.2

1) Scrapear una letra y descargar
2) Verificar una letra + primer artista
3) Mostrar estado de una letra
4) Salir
```

### 1. Scrapear una letra y descargar

El programa solicita una letra de la A a la Z. Por ejemplo, si se ingresa `m`, recorre las páginas del índice de esa letra, descubre los artistas, entra a sus páginas, extrae las canciones y descarga las versiones disponibles.

Todo el trabajo de esa ejecución se organiza dentro de:

```text
Biblioteca_LaCuerda/m/
```

Las demás letras no se recorren durante esa ejecución.

### 2. Verificar una letra

Permite hacer una prueba acotada del índice y del primer artista encontrado, sin iniciar el recorrido completo de la letra. Es útil para revisar que el sitio siga respondiendo con la estructura HTML esperada.

### 3. Mostrar estado de una letra

Consulta el control local de una letra y muestra las cantidades registradas, según la información disponible en `artistas.json`.

### 4. Salir

Cierra el programa.

## Estructura de salida

Cada letra mantiene sus propios archivos de control y carpetas de artistas:

```text
Biblioteca_LaCuerda/
└── m/
    ├── artistas.json
    ├── artistas.txt
    ├── Artista Uno/
    │   ├── Canción A - Acordes.txt
    │   └── Canción A - Tablatura.txt
    └── Artista Dos/
        └── Canción B - Acordes.txt
```

### `artistas.json`

Es el registro estructurado de la letra. Incluye, entre otros datos:

- letra procesada y URL de origen;
- páginas del índice recorridas;
- artistas descubiertos;
- URL y nombre de cada artista;
- cantidad de canciones declaradas por el índice;
- canciones encontradas, con título, enlace, identificador y `lcd`;
- resumen de páginas, artistas, canciones y versiones;
- errores detectados durante el recorrido.

El archivo se actualiza durante el proceso para conservar el avance parcial.

### `artistas.txt`

Es una versión legible del control JSON. Incluye el resumen del recorrido, el listado de artistas y canciones y los errores registrados.

### Archivos `.txt` de canciones

Cada versión se guarda por separado. Los archivos incluyen los metadatos de artista, canción, tipo de versión y URL de origen, seguidos por el contenido de acordes o tablatura.

Ejemplos:

```text
Canción A - Acordes.txt
Canción A - Tablatura.txt
Canción A - Acordes 2.txt
```

Los nombres se diferencian cuando una canción tiene varias versiones del mismo tipo, para evitar sobrescribirlas entre sí.

## Reanudar y actualizar una letra

Si se interrumpe el programa con `Ctrl+C`, se intenta terminar el ítem actual y guardar el estado parcial. Al ejecutar nuevamente esa letra:

- se reutiliza el `artistas.json` existente como punto de partida;
- se vuelven a consultar las páginas del índice de esa letra;
- se agregan los artistas nuevos encontrados;
- se conservan las canciones ya registradas mientras se actualiza la información del artista;
- se omiten los archivos de canción que ya existen;
- se vuelven a intentar las descargas que no quedaron guardadas.

**Importante:** el control JSON conserva información de ejecuciones anteriores y acumula los errores registrados. Si necesitás reconstruir desde cero el inventario de una letra, guardá una copia de su carpeta y luego decidí qué archivos de control borrar antes de volver a ejecutarla.

## Conexiones y ritmo de scraping

El programa crea una única `requests.Session()` para cada ejecución de una letra. Esto permite reutilizar conexiones HTTP cuando el servidor y las condiciones de red lo permiten; no significa que todas las peticiones deban usar necesariamente una misma conexión TCP.

Por defecto, se espera **1 segundo entre peticiones** y se usan tiempos máximos de espera para las solicitudes. Estos valores se pueden ajustar en `funciones_lc_v5.py`:

```python
TIMEOUT_SEGUNDOS = 20
TIMEOUT_REINTENTO = 30
ESPERA_ENTRE_PETICIONES = 1.0
ESPERA_ENTRE_REINTENTOS = 2.0
```

Se recomienda mantener un ritmo moderado para no generar una carga innecesaria sobre el sitio.

## Cómo está organizado el código

- **`lacuerda.py`:** contiene el menú principal y delega las acciones.
- **`funciones.py`:** implementa las peticiones HTTP, el análisis del HTML, el descubrimiento de índices y artistas, la extracción de canciones, las descargas y los archivos de control.

## Limitaciones y consideraciones

- La estructura del scraper depende del HTML que publique LaCuerda.net. Si el sitio cambia los identificadores o la organización de sus páginas, puede ser necesario adaptar los selectores.
- Una canción puede no estar disponible, responder con un error HTTP o no contener el bloque de texto esperado; esos casos se registran como errores o descargas fallidas.
- La cantidad de canciones declarada en el índice puede diferir de la cantidad extraída.
- El programa evita sobrescribir archivos existentes; por eso, si una versión ya descargada cambia en el sitio, no se reemplaza automáticamente.
- El control local representa lo que el scraper encontró y procesó; no garantiza que el índice del sitio esté completo ni que todas las transcripciones estén disponibles.

## Historial de versiones

### v5.2

- Se incorpora la selección interactiva de una letra del índice alfabético.
- Cada letra guarda su inventario y sus canciones en una carpeta independiente.
- Los archivos `artistas.json` y `artistas.txt` quedan separados por letra.
- Las opciones del menú permiten ejecutar, verificar y consultar el estado de una letra.

### v5.1

- Se integra el descubrimiento de artistas con el descargador de canciones.
- Se reutiliza una `requests.Session()` durante el recorrido.
- Se mantiene el control JSON/TXT y la descarga de versiones a archivos `.txt`.

### v4

- Descarga de canciones a partir de un `lista.html` local con la lista de canciones de un artista.
- Soporte para múltiples versiones.
- Validación de la ruta del artista, reintentos y escritura atómica.
- Menú para descargar/actualizar, verificar la lista y consultar el estado.

## Licencia

Este proyecto se distribuye bajo la licencia **GNU General Public License v3.0 (GPL-3.0)**. Consultá el archivo `LICENSE` incluido en el repositorio para ver el texto completo de la licencia.
