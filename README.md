# 🎸 Biblioteca LaCuerda v5.3

Crawler y descargador de acordes y tablaturas de [acordes.lacuerda.net](https://acordes.lacuerda.net).
Recorre el índice alfabético del sitio, descubre artistas y canciones, y guarda cada versión
(acordes, tablatura, bajo, armónica, teclado) como un archivo `.txt`.

```
índice alfabético → páginas indexXXX → artistas → canciones → versiones → archivos TXT
```

---

## Contenido del proyecto

| Archivo | Rol |
|---|---|
| `lacuerda.py` | Lanzador. Muestra un menú interactivo por consola y llama a las funciones del módulo. |
| `funciones.py` | Toda la lógica: peticiones HTTP, parseo del HTML, control de estado, descarga y guardado. |

---

## Requisitos

- Python 3.8 o superior
- Librerías externas:

```bash
pip install requests beautifulsoup4
```

El resto de módulos (`json`, `os`, `re`, `signal`, `time`, etc.) son de la biblioteca estándar.

---

## Uso

```bash
python lacuerda.py
```

Se abre el menú:

```
╔══════════════════════════════════════════════════╗
║              Biblioteca LaCuerda v5.3            ║
║     Índices → Artistas → Canciones → TXT         ║
╚══════════════════════════════════════════════════╝

  1) Scrapear una letra y descargar
  2) Verificar una letra + primer artista
  3) Mostrar estado de una letra
  4) Reintentar fallidas de una letra (índices, artistas, versiones)
  5) Salir
```

| Opción | Qué hace |
|---|---|
| **1** | Pide una letra (A-Z) y descarga todos los artistas y canciones de esa letra. |
| **2** | Prueba rápida: consulta la primera página del índice de una letra y el primer artista, sin descargar canciones. Útil para comprobar que el sitio responde y que el parseo sigue funcionando. |
| **3** | Muestra el resumen guardado (contadores) de una letra procesada anteriormente. |
| **4** | Reintenta **solo lo que falló** en una letra (páginas de índice, páginas de artista y versiones sueltas), leyendo `registro_resultados.json`, sin recorrer de nuevo lo que ya salió bien. |
| **5** | Sale del programa. |

Después de cada acción, el programa espera un Enter para volver al menú.

### Reintentar solo las fallidas (opción 4)

Al terminar una letra, el programa informa cuántos índices, artistas y versiones fallaron.
La opción 4 los reintenta en este orden, sin tocar lo que ya salió bien:

1. **Páginas de índice**: si una se recupera, descubre sus artistas y las páginas de índice que faltaban.
2. **Versiones sueltas**: vuelve a pedir solo esas URLs.
3. **Páginas de artista**: las recuperadas (y los artistas nuevos del paso 1) descargan todas sus canciones, omitiendo los archivos que ya existen.

Lo que se resuelve sale del registro y de la lista de errores de `artistas.json`; lo que sigue fallando conserva su motivo y suma un intento.

Si la letra se procesó con una versión anterior y no tiene registro, la opción 4 lo reconstruye sin red a partir de `artistas.json`
(errores de índice, artistas con error) y de los `.txt` que existen en disco.

> Un artista que quedó sin procesar porque cortaste la ejecución (sin error) no cuenta como fallido: se retoma volviendo a ejecutar la opción 1.

### Interrumpir y reanudar

- **Ctrl+C una vez**: termina el ítem en curso, guarda el control parcial y sale de forma ordenada.
- **Ctrl+C dos veces**: corte inmediato.
- Para **reanudar**, simplemente volvé a ejecutar la opción 1 con la misma letra: lee el `artistas.json`
  existente, conserva lo ya descubierto y **omite los archivos `.txt` que ya existen**.

---

## Estructura de salida

Cada letra tiene su propia carpeta, así se pueden actualizar de forma independiente:

```
Biblioteca_LaCuerda/
└── a/
    ├── artistas.json          # estado completo (se usa para reanudar)
    ├── artistas.txt           # reporte de control legible
    ├── registro_resultados.json  # resultado de índices, artistas y versiones
    ├── registro_resultados.txt   # el mismo registro en texto legible
    ├── Nombre_Artista/
    │   ├── Cancion - Acordes.txt
    │   ├── Cancion - Tablatura.txt
    │   └── Otra cancion - Acordes 1.txt
    └── ...
```

### Formato de cada `.txt` descargado

```
ARTISTA: Nombre del artista
CANCION: Título
VERSION: Acordes
URL: https://acordes.lacuerda.net/artista/cancion.shtml
========================================

<contenido de la canción>
```

Si una canción tiene varias versiones del mismo tipo, se numeran (`Acordes 1`, `Acordes 2`, ...).

### Archivos de control

- **`artistas.json`**: versión, fuente, fecha de inicio/fin, páginas de índice vistas, artistas con sus
  canciones, errores y un bloque `resumen` con los contadores.
- **`artistas.txt`**: el mismo estado en texto plano: resumen, lista de artistas con sus canciones
  y sección de errores.

- **`registro_resultados.json` / `.txt`**: registra lo que salió mal y lo que salió bien en cada letra:
  - `indices_fallidos`: páginas de índice (`indexN.html`) que no se pudieron leer.
  - `artistas_fallidos`: páginas de artista que no se pudieron leer.
  - `fallidas`: versiones (acordes, tablatura, etc.) que no se pudieron guardar.
  - `descargadas`: versiones guardadas, con fecha y origen (`descarga`, `existente` o `reintento`).

  Cada fallo guarda el motivo, la cantidad de intentos y la fecha del último. La opción 4 trabaja sobre este registro.

Todos se escriben de forma **atómica** (archivo temporal + `os.replace`), por lo que un corte
inesperado no deja archivos a medio escribir.

#### Contadores del resumen

| Campo | Significado |
|---|---|
| `paginas_indice` | Páginas de índice recorridas |
| `artistas_encontrados` | Artistas detectados en el índice |
| `artistas_procesados` | Artistas cuya página se descargó sin error |
| `canciones_encontradas` | Canciones listadas en las páginas de artistas |
| `versiones_descargadas` | Archivos `.txt` nuevos guardados |
| `versiones_omitidas` | Archivos que ya existían |
| `versiones_fallidas` | Versiones que no se pudieron guardar |

---

## Cómo funciona

1. **Índice**: pide `https://acordes.lacuerda.net/tabs/<letra>/index0.html` y detecta las demás
   páginas de paginación (`indexN.html`) desde el bloque `.multipag`.
2. **Artistas**: extrae nombre, URL y cantidad de canciones declarada desde `ul#i_main`.
3. **Canciones**: en la página de cada artista lee `ul#b_main`. Si la cantidad declarada no coincide con
   la encontrada, lo registra como `advertencia_cantidad`.
4. **Versiones**: el atributo `lcd` de cada canción (por ejemplo `RT-12`) codifica los tipos y números de
   versión disponibles y se traduce a las URLs correspondientes.
5. **Descarga**: extrae el contenido del `<pre>` de cada página y lo guarda en el `.txt`.

### Tipos de versión

| Código | Tipo |
|---|---|
| `R` | Acordes |
| `T` | Tablatura |
| `B` | Bajo |
| `H` | Armónica |
| `K` | Teclado |

### Manejo de errores

- Mensajes en lenguaje claro para timeouts, fallas de conexión y códigos HTTP comunes (403, 404, 429, 5xx).
- Los errores de conexión o timeout se **reintentan al final de cada artista**, con un timeout mayor.
- Todos los errores quedan registrados en la sección `errores` del JSON y del TXT de control.

---

## Configuración

Las constantes están al inicio de `funciones.py`:

| Constante | Valor por defecto | Descripción |
|---|---|---|
| `CARPETA_PRINCIPAL` | `Biblioteca_LaCuerda` | Carpeta raíz de salida |
| `ESPERA_ENTRE_PETICIONES` | `1.0` | Segundos de pausa entre peticiones |
| `ESPERA_ENTRE_REINTENTOS` | `2.0` | Pausa antes de cada reintento |
| `TIMEOUT_SEGUNDOS` | `20` | Timeout de una petición normal |
| `TIMEOUT_REINTENTO` | `30` | Timeout de un reintento |
| `LETRAS` | `a-z` | Letras válidas del índice |
| `HEADERS` | User-Agent de navegador | Cabeceras de la sesión HTTP |

---

## Referencia rápida de `funciones.py`

| Grupo | Funciones principales |
|---|---|
| Interrupciones | `instalar_manejador_interrupciones` |
| HTTP | `crear_sesion`, `obtener`, `esperar`, `mensaje_amigable_error`, `mensaje_amigable_codigo` |
| Utilidades | `nombre_seguro`, `slugify_artista`, `escribir_json_atomico`, `escribir_texto_atomico` |
| Estado y control | `nuevo_estado`, `cargar_estado_letra`, `construir_txt_control`, `guardar_control` |
| Índices | `url_indice`, `extraer_paginas_indice`, `extraer_artistas_indice`, `obtener_indice` |
| Artistas y canciones | `extraer_canciones_artista`, `parsear_versiones`, `descargar_pagina_artista` |
| Descarga | `guardar_version_si_corresponde`, `descargar_canciones_artista` |
| Registro de resultados | `nuevo_registro`, `cargar_registro_letra`, `guardar_registro`, `registrar_descarga`, `registrar_fallo`, `registrar_fallo_en`, `reconstruir_registro` |
| Flujo principal | `procesar_letra`, `procesar_pagina_indice`, `procesar_artista`, `reintentar_fallidas`, `verificar_indice_a`, `mostrar_estado`, `pedir_letra` |

---

## Buenas prácticas y aviso

- Mantené la pausa entre peticiones (`ESPERA_ENTRE_PETICIONES`) para no sobrecargar el servidor.
  Si recibís errores `429`, aumentala.
- El scraping depende de la estructura HTML actual del sitio (`i_main`, `b_main`, `multipag`, `tbody`).
  Si el sitio cambia su diseño, hay que ajustar los selectores en `funciones.py`.
- Las letras de canciones y acordes pertenecen a sus autores y al sitio de origen. Usá este material
  solo para uso personal y respetá los términos de uso de LaCuerda.
