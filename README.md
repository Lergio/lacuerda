# 🎸 Biblioteca LaCuerda

Script en Python para automatizar la creación de una biblioteca local de **acordes, tablaturas, bajo, armónica y teclado** a partir de listas de canciones de [LaCuerda.net](https://lacuerda.net/).

El programa analiza un archivo `lista.html`, identifica automáticamente el artista y las canciones disponibles, detecta las diferentes versiones de cada tema y descarga cada transcripción como un archivo `.txt` organizado por artista.

---

## 📋 Características

* 🎤 **Detección automática del artista** desde `lista.html`.
* ⌨️ Posibilidad de indicar el artista manualmente mediante argumentos de consola o `input`.
* 🔤 Generación automática del **slug utilizado por LaCuerda** para las URLs.
* 🌎 Manejo de tildes y caracteres especiales.
* 🅰️ Tratamiento especial para artistas cuyo nombre comienza con `El`, `La`, `Los` o `Las`.
* 🔎 Verificación automática de la ruta del artista antes de iniciar la descarga.
* ✏️ Posibilidad de introducir manualmente la ruta correcta si no puede determinarse automáticamente.
* 🎵 Detección de canciones a partir de los enlaces presentes en `lista.html`.
* 🧹 Eliminación de canciones duplicadas.
* 🎼 Detección de múltiples versiones de una misma canción.
* 🎸 Identificación de diferentes tipos de transcripción:

  * Acordes
  * Tablatura
  * Bajo
  * Armónica
  * Teclado
* 📄 Generación de un archivo `.txt` independiente para cada versión.
* 🔄 Evita volver a descargar archivos que ya existen.
* 🌐 Manejo de errores HTTP y fallos de conexión.
* 🔁 Permite corregir manualmente la ruta del artista y reiniciar el proceso si se detecta un `404`.
* 📊 Muestra un resumen final de las versiones descargadas y omitidas.

---

## 🛠️ Requisitos

Se necesita:

* **Python 3.8 o superior**
* `requests`
* `beautifulsoup4`

Las librerías externas pueden instalarse con:

```bash
pip install requests beautifulsoup4
```

---

## 📁 Estructura del proyecto

La estructura mínima necesaria es:

```text
scraps_lacuerda/
│
├── lacuerda.py
└── lista.html
```

La carpeta de la biblioteca se crea automáticamente.

Después de ejecutar el programa:

```text
scraps_lacuerda/
│
├── lacuerda.py
├── lista.html
│
└── Biblioteca_LaCuerda/
    │
    └── Nombre_Artista/
        ├── Cancion 1 - Acordes.txt
        ├── Cancion 1 - Tablatura.txt
        ├── Cancion 2 - Acordes.txt
        └── ...
```

---

## 🚀 Uso

### 1. Preparar `lista.html`

El programa necesita un archivo llamado:

```text
lista.html
```

Este archivo debe contener la lista de canciones obtenida de LaCuerda.

El programa analiza los elementos `<li>` y busca los enlaces `<a>` correspondientes a las canciones.

Además, puede obtener automáticamente el nombre del artista cuando el HTML contiene información como:

```html
<script>
    bName = 'Abel Pintos'
</script>
```

---

### 2. Ejecutar normalmente

Desde la carpeta del proyecto:

```bash
python lacuerda.py
```

Si `lista.html` contiene el nombre del artista, el programa intentará detectarlo automáticamente.

---

### 3. Indicar el artista manualmente

También es posible pasar el nombre del artista como argumento:

```bash
python lacuerda.py "Abel Pintos"
```

Esto resulta útil cuando `lista.html` no contiene la información `bName`.

---

## 🎤 Detección del artista

El programa utiliza tres métodos para determinar el artista, en este orden:

1. Busca automáticamente `bName` dentro de `lista.html`.
2. Si no lo encuentra, utiliza los argumentos proporcionados al ejecutar el programa.
3. Si tampoco existen argumentos, solicita el nombre mediante `input`.

Una vez obtenido el nombre, genera automáticamente los posibles slugs utilizados por LaCuerda.

Por ejemplo:

```text
Abel Pintos
```

se convierte en:

```text
abel_pintos
```

El programa también contempla casos especiales con `ñ`, tildes y artículos iniciales. Por ejemplo, tiene en cuenta que determinados nombres pueden utilizar una representación diferente en las URLs del sitio.

---

## 🌐 Verificación de la URL del artista

Antes de iniciar la descarga masiva, el programa prueba la ruta del artista utilizando la primera canción encontrada.

Por ejemplo:

```text
https://acordes.lacuerda.net/abel_pintos/cancion.shtml
```

Si responde correctamente, esa ruta se utiliza para el resto de las canciones.

Si el nombre contiene un artículo inicial, como:

```text
Los Pericos
```

también puede probar automáticamente:

```text
los_pericos
```

y:

```text
pericos
```

Si ninguna de las rutas funciona, el programa solicita manualmente el tramo correcto de la URL.

---

## 🎵 Procesamiento de canciones

Las canciones se obtienen recorriendo los elementos `<li>` de `lista.html`.

El programa extrae:

* El `href` de la canción.
* El título.
* El atributo `lcd`, utilizado por LaCuerda para identificar las diferentes versiones.

Las canciones se almacenan internamente utilizando su `slug`, evitando procesar dos veces el mismo enlace aunque aparezca repetido dentro del HTML.

---

## 🎼 Múltiples versiones

Una de las principales funcionalidades del proyecto es el procesamiento de múltiples versiones de una misma canción.

El atributo `lcd` puede contener información como:

```text
RRTKT-12534
```

Las letras representan diferentes tipos de transcripción y los números indican qué versión corresponde a cada una.

El programa interpreta esa información y genera las URLs correspondientes.

Los tipos actualmente reconocidos son:

| Código | Tipo      |
| ------ | --------- |
| `R`    | Acordes   |
| `T`    | Tablatura |
| `B`    | Bajo      |
| `H`    | Armónica  |
| `K`    | Teclado   |

Si una canción posee varias versiones del mismo tipo, se utiliza un contador para evitar sobrescribir archivos.

Por ejemplo:

```text
Cancion - Acordes.txt
Cancion - Acordes 2.txt
Cancion - Tablatura.txt
```

---

## 📄 Archivos generados

Cada versión se guarda en un archivo independiente.

Por ejemplo:

```text
Biblioteca_LaCuerda/
└── Abel_Pintos/
    ├── La_Llave - Acordes.txt
    ├── La_Llave - Tablatura.txt
    └── La_Llave - Bajo.txt
```

Cada archivo contiene información de identificación antes del contenido de la transcripción:

```text
ARTISTA: Abel Pintos
CANCION: La Llave
VERSION: Acordes
URL: https://acordes.lacuerda.net/abel_pintos/la_llave.shtml
========================================

[Contenido de la canción]
```

Esto permite conocer posteriormente de dónde provino cada archivo y qué tipo de versión contiene.

---

## 🔎 Extracción del contenido

Para obtener el contenido de las canciones, el programa busca primero el contenedor principal de LaCuerda:

```html
<div id="tbody">
```

o:

```html
<div id="t_body">
```

Dentro de ese contenedor busca una etiqueta:

```html
<pre>
```

Si no encuentra el contenedor principal, utiliza un `<pre>` directamente como alternativa.

Esto permite conservar los espacios y la alineación del contenido, algo especialmente importante para las tablaturas y los acordes.

---

## 🔄 Archivos existentes

El programa comprueba si el archivo correspondiente a una versión ya existe:

```python
if os.path.exists(ruta_final_txt):
```

Cuando encuentra un archivo existente, lo omite y continúa con la siguiente versión.

Esto permite ejecutar nuevamente el programa sin tener que descargar toda la biblioteca desde cero.

Ejemplo:

```text
[1/100] Cancion 1
[2/100] Cancion 2
[3/100] Cancion 3
```

Las versiones que ya existen no se vuelven a descargar.

---

## ⚠️ Manejo de errores

El programa contempla diferentes situaciones.

### `lista.html` inexistente

```text
❌ Error: No se encuentra el archivo 'lista.html'
```

### Ruta del artista incorrecta

El programa prueba automáticamente diferentes posibilidades.

Si ninguna funciona, solicita al usuario la ruta correcta.

### Error `404`

Si durante la primera descarga real aparece un `404`, el programa puede solicitar una nueva ruta de artista y reiniciar el recorrido.

### Fallos de conexión

Los errores de conexión se muestran en consola y el programa continúa procesando las siguientes versiones.

### Contenido no encontrado

Si una página responde correctamente pero no contiene el contenido esperado, se muestra una advertencia:

```text
⚠️ No se encontró el texto de la canción
```

---

## ⏱️ Pausa entre solicitudes

El programa utiliza una pausa de:

```python
time.sleep(2)
```

entre las solicitudes de descarga.

Esto reduce la frecuencia de peticiones realizadas al sitio y evita ejecutar una descarga masiva de manera demasiado agresiva.

---

## 📊 Resumen final

Al finalizar el proceso se muestra un resumen:

```text
--- RESUMEN ---
Versiones descargadas: 150
Versiones omitidas (ya existían): 35
```

Esto permite conocer rápidamente cuánto contenido nuevo se agregó a la biblioteca.

---

## 🧩 Dependencias

El proyecto utiliza las siguientes librerías:

| Librería        | Uso                                                 |
| --------------- | --------------------------------------------------- |
| `os`            | Manejo de archivos y directorios                    |
| `re`            | Expresiones regulares y procesamiento de texto      |
| `sys`           | Argumentos de línea de comandos                     |
| `time`          | Pausas entre solicitudes                            |
| `unicodedata`   | Normalización de caracteres y eliminación de tildes |
| `requests`      | Solicitudes HTTP                                    |
| `BeautifulSoup` | Análisis y extracción del HTML                      |

Las librerías `os`, `re`, `sys`, `time` y `unicodedata` forman parte de la biblioteca estándar de Python.

Las dependencias externas son:

```text
requests
beautifulsoup4
```

---

## 🔧 Configuración

La configuración general se encuentra al comienzo de `lacuerda.py`:

```python
CARPETA_PRINCIPAL = "Biblioteca_LaCuerda"
ARCHIVO_HTML_LOCAL = "lista.html"
DOMINIO_BASE = "https://acordes.lacuerda.net"
```

### Carpeta principal

```python
CARPETA_PRINCIPAL = "Biblioteca_LaCuerda"
```

Define dónde se almacenará la biblioteca descargada.

### Archivo HTML

```python
ARCHIVO_HTML_LOCAL = "lista.html"
```

Define el archivo que contiene la lista de canciones.

### Dominio

```python
DOMINIO_BASE = "https://acordes.lacuerda.net"
```

Define el dominio utilizado para construir las URLs de las canciones.

---

## 📂 Organización de la biblioteca

El objetivo es mantener una estructura organizada por artista:

```text
Biblioteca_LaCuerda/
│
├── Abel_Pintos/
│   ├── Aventura - Acordes.txt
│   ├── Aventura - Tablatura.txt
│   └── ...
│
├── Attaque_77/
│   ├── Arrancacorazones - Acordes.txt
│   └── ...
│
└── Los_Pericos/
    ├── Sin_Cadenas - Acordes.txt
    └── ...
```

De esta manera, una única biblioteca puede contener material de múltiples artistas.

---

## 🔒 Uso responsable

Este proyecto automatiza solicitudes hacia un sitio web externo.

Se recomienda:

* Respetar los términos de uso del sitio.
* Respetar `robots.txt` y cualquier restricción aplicable.
* Mantener una frecuencia razonable de solicitudes.
* Utilizar las pausas incorporadas por el programa.
* Utilizar el contenido descargado de acuerdo con los derechos de autor correspondientes.
* No redistribuir contenido protegido sin la autorización necesaria.

El proyecto automatiza el procesamiento y organización de contenido; los derechos sobre dicho contenido pertenecen a sus respectivos titulares.

---

## 🚧 Estado actual

El proyecto se encuentra en desarrollo y continúa evolucionando mediante commits y versiones.

La versión actual se centra en:

* Automatización de la detección del artista.
* Generación de URLs.
* Procesamiento de múltiples versiones.
* Descarga y organización de transcripciones.
* Manejo de diferentes estructuras de URL.
* Prevención de archivos duplicados.
* Recuperación ante errores de rutas.

---

## 💡 Próximas mejoras

Algunas mejoras que podrían incorporarse en futuras versiones:

* [ ] Procesamiento automático de múltiples artistas.
* [ ] Generación de un índice general de canciones.
* [ ] Registro de errores en archivos `.log`.
* [ ] Sistema de reintentos para conexiones fallidas.
* [ ] Mejor manejo de códigos HTTP.
* [ ] Detección de cambios en canciones ya descargadas.
* [ ] Interfaz gráfica.
* [ ] Opciones de configuración mediante archivo externo.
* [ ] Generación de diferentes formatos de salida.
* [ ] Estadísticas más detalladas de la biblioteca.

---

## 📜 Licencia

El código de este proyecto puede ser utilizado y modificado de acuerdo con la licencia definida en el repositorio.

El contenido descargado mediante el programa puede estar sujeto a derechos de autor y a las condiciones de uso de LaCuerda.net.

La licencia del código y los derechos sobre las tablaturas, acordes y demás contenido descargado deben considerarse por separado.

---

## 🎸 Objetivo del proyecto

El objetivo de **Biblioteca LaCuerda** es automatizar una tarea repetitiva: transformar listas de canciones disponibles en LaCuerda en una biblioteca local organizada, manteniendo separadas las diferentes versiones y tipos de transcripción.

```text
lista.html
     │
     ▼
Detectar artista
     │
     ▼
Resolver URL
     │
     ▼
Detectar canciones
     │
     ▼
Detectar versiones
     │
     ▼
Descargar contenido
     │
     ▼
Biblioteca_LaCuerda/
     │
     └── Artista/
           ├── Canción - Acordes.txt
           ├── Canción - Tablatura.txt
           └── Canción - Bajo.txt
```
