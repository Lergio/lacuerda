# 🎸 Biblioteca LaCuerda

Script en Python para automatizar la creación de una biblioteca local de **acordes, tablaturas, bajo, armónica y teclado** a partir de listas de canciones de [LaCuerda.net](https://lacuerda.net/).

El programa analiza un archivo `lista.html`, identifica automáticamente el artista y las canciones disponibles, detecta las diferentes versiones de cada tema y descarga cada transcripción como un archivo `.txt` organizado por artista.

Además, incorpora mecanismos para **interrumpir y reanudar el proceso de forma segura**, reintentar automáticamente algunos errores de conexión y evitar archivos incompletos o corruptos.

---

## 📋 Características

* 🎤 **Detección automática del artista** desde `lista.html`.
* ⌨️ Posibilidad de indicar el artista mediante argumentos de consola o `input`.
* 🔤 Generación automática del **slug utilizado por LaCuerda** para las URLs.
* 🌎 Manejo de tildes y caracteres especiales.
* `ñ` convertida específicamente al formato utilizado por LaCuerda.
* 🅰️ Tratamiento especial para artistas cuyo nombre comienza con `El`, `La`, `Los` o `Las`.
* 🔎 Verificación automática de la ruta del artista antes de comenzar la descarga masiva.
* ✏️ Posibilidad de introducir manualmente la ruta correcta del artista.
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
* 🚫 Evita volver a descargar archivos que ya existen.
* 💾 **Escritura atómica de archivos**, evitando dejar `.txt` incompletos si el proceso se interrumpe.
* 🛑 **Interrupción segura mediante `Ctrl+C`**.
* 🔁 Reanudación automática al volver a ejecutar el programa.
* 🌐 Manejo de errores HTTP.
* ⏱️ Reintento automático de timeouts y errores de conexión transitorios.
* 🔄 Segundo intento con un tiempo de espera mayor para las versiones que fallaron temporalmente.
* 📊 Resumen final con descargas, archivos omitidos y versiones que continuaron fallando.
* 💬 Mensajes de error más claros y comprensibles.

---

## 🛠️ Requisitos

Se necesita:

* **Python 3.8 o superior**
* `requests`
* `beautifulsoup4`

Instalar las dependencias externas:

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

Este archivo debe contener la lista de canciones que se desea procesar.

El programa analiza los elementos `<li>` y busca los enlaces `<a>` correspondientes a las canciones.

También puede obtener automáticamente el nombre del artista cuando el HTML contiene información como:

```html
<script>
    bName = 'Abel Pintos'
</script>
```

---

### 2. Ejecutar el programa

Desde la carpeta del proyecto:

```bash
python lacuerda.py
```

Si `lista.html` contiene el nombre del artista, el programa intentará detectarlo automáticamente.

---

### 3. Indicar el artista manualmente

Si `lista.html` no contiene `bName`, también se puede indicar el nombre del artista desde la línea de comandos:

```bash
python lacuerda.py "Abel Pintos"
```

Si tampoco se proporciona un argumento, el programa solicitará el nombre mediante `input`.

---

## 🎤 Detección del artista

El programa utiliza tres métodos para determinar el artista, en este orden:

1. Busca automáticamente `bName` dentro de `lista.html`.
2. Si no lo encuentra, utiliza los argumentos proporcionados al ejecutar el programa.
3. Si tampoco existen argumentos, solicita el nombre mediante `input`.

Una vez obtenido el nombre, genera automáticamente los posibles `slug` utilizados por LaCuerda.

Por ejemplo:

```text
Abel Pintos
```

se convierte en:

```text
abel_pintos
```

### Tratamiento de `ñ`

LaCuerda utiliza una representación particular para algunos nombres que contienen `ñ`.

Por ejemplo:

```text
Chaqueño
```

se transforma en:

```text
chaquenio
```

El programa realiza esta conversión antes de eliminar las tildes y normalizar el resto de los caracteres.

---

## 🌐 Resolución de la URL del artista

El programa genera una o más rutas candidatas para el artista y las prueba antes de iniciar la descarga masiva.

Por ejemplo, para:

```text
Los Pericos
```

puede probar:

```text
los_pericos
```

y:

```text
pericos
```

Esto permite contemplar los casos en los que LaCuerda omite el artículo inicial del nombre del artista.

La ruta se verifica utilizando la primera canción encontrada en `lista.html`.

Si una ruta responde correctamente, se utiliza para generar las URLs del resto de las canciones.

---

## ✏️ Corrección manual de la ruta

Si ninguno de los `slug` generados automáticamente funciona, el programa solicita al usuario el tramo correcto de la URL.

Por ejemplo:

```text
https://acordes.lacuerda.net/bersuit/
```

En ese caso se debe introducir:

```text
bersuit
```

El programa vuelve a comprobar la ruta antes de continuar.

Además, si durante la primera descarga real se encuentra un `404`, el programa vuelve a solicitar la ruta correcta y reinicia el recorrido.

---

## 🎵 Procesamiento de canciones

Las canciones se obtienen recorriendo los elementos `<li>` de `lista.html`.

Para cada canción se extrae:

* El `href`.
* El título.
* El atributo `lcd`.

El título se limpia para eliminar información adicional incluida dentro de etiquetas `<em>`, como:

```text
acordes
tablatura
```

Las canciones se almacenan utilizando su `slug`, evitando procesar dos veces el mismo enlace aunque aparezca repetido dentro del HTML.

---

## 🎼 Múltiples versiones

El programa interpreta el atributo `lcd` para determinar qué versiones existen para cada canción.

Por ejemplo:

```text
RRTKT-12534
```

se interpreta asociando cada letra con el número correspondiente.

Los tipos actualmente reconocidos son:

| Código | Tipo      |
| ------ | --------- |
| `R`    | Acordes   |
| `T`    | Tablatura |
| `B`    | Bajo      |
| `H`    | Armónica  |
| `K`    | Teclado   |

El número `1` representa la URL sin sufijo:

```text
cancion.shtml
```

Mientras que los siguientes números generan:

```text
cancion-2.shtml
cancion-3.shtml
cancion-4.shtml
```

Las versiones se ordenan por su número antes de comenzar la descarga.

Si aparece una letra de tipo que el programa todavía no conoce, se conserva esa letra como etiqueta en lugar de descartarla.

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

Si existen varias versiones del mismo tipo, se agregan números para evitar sobrescribir archivos:

```text
Cancion - Acordes 1.txt
Cancion - Acordes 2.txt
Cancion - Acordes 3.txt
```

Cuando solo existe una versión de un tipo, se utiliza:

```text
Cancion - Acordes.txt
```

---

## 📝 Contenido de los archivos

Cada archivo contiene información de identificación antes de la transcripción:

```text
ARTISTA: Abel Pintos
CANCION: La Llave
VERSION: Acordes
URL: https://acordes.lacuerda.net/abel_pintos/la_llave.shtml
========================================

[Contenido de la canción]
```

Esto permite conocer posteriormente:

* Artista.
* Canción.
* Tipo de versión.
* URL de origen.
* Contenido de la transcripción.

---

## 🔎 Extracción del contenido

Para obtener el contenido de cada canción, el programa busca primero los contenedores principales:

```html
<div id="tbody">
```

o:

```html
<div id="t_body">
```

Dentro del contenedor busca:

```html
<pre>
```

Si no encuentra el contenedor principal, utiliza como alternativa cualquier `<pre>` disponible en la página.

El uso de `.text` permite eliminar las etiquetas HTML internas manteniendo los espacios y la alineación del contenido, algo especialmente importante para los acordes y las tablaturas.

---

# 💾 Escritura segura de archivos

Una de las mejoras de esta versión es la escritura **atómica** de los archivos.

En lugar de escribir directamente sobre:

```text
Cancion - Acordes.txt
```

el programa primero crea:

```text
Cancion - Acordes.txt.tmp
```

Escribe y sincroniza el contenido y, solamente cuando termina correctamente, reemplaza el archivo definitivo.

Esto evita que una interrupción, un corte de luz o un fallo del proceso deje un `.txt` parcialmente escrito que posteriormente sea interpretado como una descarga completa.

La implementación se encuentra en la función `escribir_archivo_atomico()`.

---

# 🛑 Interrupción segura

El programa incorpora manejo de señales para permitir detener la ejecución mediante:

```text
Ctrl+C
```

Al presionar `Ctrl+C` una vez, el programa no corta inmediatamente la operación.

En cambio:

1. Marca que se solicitó detener el proceso.
2. Termina el elemento que está procesando.
3. Guarda correctamente cualquier archivo que corresponda.
4. Muestra un resumen parcial.
5. Finaliza de forma ordenada.

El mensaje mostrado es:

```text
🛑 Se pidió detener el script...
Terminando la descarga en curso y cerrando de forma prolija...
```

Si se presiona `Ctrl+C` nuevamente, se realiza un corte forzado.

---

# ▶️ Continuar una descarga interrumpida

Una de las ventajas de esta versión es que se puede volver a ejecutar el programa después de detenerlo.

Los archivos que ya fueron descargados se detectan automáticamente:

```python
if os.path.exists(ruta_final_txt):
```

y se omiten.

Por lo tanto, si una biblioteca tenía 500 versiones para descargar y el proceso se detuvo después de 200, al volver a ejecutar:

* Las 200 ya existentes se omiten.
* Las restantes continúan procesándose.

Esto permite utilizar el script de manera mucho más segura con bibliotecas grandes.

---

# 🌐 Manejo de errores de conexión

Los errores de red se clasifican para mostrar mensajes más fáciles de interpretar.

### Timeout

Si el servidor tarda demasiado:

```text
⏱️ el servidor tardó demasiado en responder
```

### Error de conexión

Si no se puede establecer conexión:

```text
⏱️ no se pudo establecer conexión con el servidor
```

### Otros errores de red

Se informa:

```text
❌ hubo un problema de conexión
```

---

# 🔁 Sistema de reintentos

Los `timeout` y errores de conexión se consideran errores potencialmente transitorios.

En lugar de descartarlos inmediatamente, el programa los coloca en una lista de pendientes:

```text
pendientes_reintento
```

El recorrido principal continúa normalmente.

Cuando termina la primera pasada, el programa realiza una segunda pasada exclusivamente con las versiones que fallaron por problemas de conexión.

Durante este segundo intento utiliza un timeout mayor:

```text
Primer intento: 15 segundos
Reintento:      25 segundos
```

Si una versión finalmente se descarga correctamente, se guarda normalmente.

Si vuelve a fallar, se informa en el resumen final.

---

# ⚠️ Códigos HTTP

El programa proporciona mensajes más claros para algunos códigos HTTP:

| Código | Significado mostrado                     |
| ------ | ---------------------------------------- |
| `403`  | Acceso rechazado por el servidor         |
| `404`  | La página no existe                      |
| `500`  | Error interno del servidor               |
| `502`  | Servidor no disponible momentáneamente   |
| `503`  | Servicio no disponible en este momento   |
| `504`  | El servidor tardó demasiado en responder |

Otros códigos se muestran como un rechazo genérico de la solicitud.

---

# ⏱️ Pausa entre solicitudes

Entre las solicitudes se mantiene una pausa de:

```python
time.sleep(2)
```

Esto evita realizar todas las peticiones de manera consecutiva y ayuda a mantener una frecuencia moderada de solicitudes.

El mismo intervalo se utiliza durante los reintentos.

---

# 🚫 Archivos existentes

Si el archivo correspondiente a una versión ya existe, el programa lo omite:

```text
Cancion - Acordes.txt
```

No vuelve a descargarlo.

Esto permite:

* Reanudar procesos interrumpidos.
* Ejecutar nuevamente el script.
* Actualizar una biblioteca sin descargar nuevamente todo su contenido.
* Evitar sobrescribir archivos existentes.

---

# 📊 Resumen final

Al terminar el recorrido, el programa muestra un resumen.

Ejemplo:

```text
--- RESUMEN ---
Versiones descargadas: 150
Versiones omitidas (ya existían): 35
Versiones que siguieron fallando tras el reintento: 4
```

Si el proceso fue detenido mediante `Ctrl+C`, se informa además:

```text
⏸️ Detenido por el usuario antes de terminar.
Podés volver a correr el script: las canciones ya descargadas
se saltean automáticamente y continúa desde donde quedó.
```

---

# 🔧 Configuración

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

Define dónde se almacenará la biblioteca.

### Archivo HTML

```python
ARCHIVO_HTML_LOCAL = "lista.html"
```

Define el archivo que contiene la lista de canciones.

### Dominio

```python
DOMINIO_BASE = "https://acordes.lacuerda.net"
```

Define el dominio utilizado para construir las URLs.

---

# 📂 Organización de la biblioteca

La biblioteca se organiza por artista:

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

Cada ejecución trabaja con **un artista asociado al `lista.html` utilizado**.

El programa organiza las canciones de ese artista dentro de su carpeta correspondiente.

---

# 🧩 Dependencias

El proyecto utiliza módulos de la biblioteca estándar de Python:

* `os`
* `re`
* `signal`
* `sys`
* `time`
* `unicodedata`

Y dos dependencias externas:

* `requests`
* `beautifulsoup4`

Instalación:

```bash
pip install requests beautifulsoup4
```

---

# 🔒 Uso responsable

Este proyecto automatiza solicitudes hacia un sitio web externo.

Se recomienda:

* Respetar los términos de uso del sitio.
* Respetar `robots.txt` y cualquier restricción aplicable.
* Mantener una frecuencia razonable de solicitudes.
* No eliminar la pausa entre solicitudes sin una razón válida.
* Utilizar el contenido descargado de acuerdo con los derechos de autor correspondientes.
* No redistribuir contenido protegido sin la autorización necesaria.

El proyecto automatiza el procesamiento y organización del contenido; los derechos sobre dicho contenido pertenecen a sus respectivos titulares.

---

# 🚧 Estado actual

La versión actual incorpora:

* Detección automática del artista.
* Generación y validación de rutas.
* Procesamiento de múltiples versiones.
* Descarga de diferentes tipos de transcripción.
* Prevención de archivos duplicados.
* Escritura atómica.
* Interrupción segura.
* Reanudación del proceso.
* Manejo de errores HTTP.
* Reintentos de errores de conexión.
* Resumen detallado de resultados.

---

# 💡 Próximas mejoras

Algunas posibles mejoras para futuras versiones:

* [ ] Procesamiento automático de múltiples artistas.
* [ ] Generación de un índice general de canciones.
* [ ] Registro de errores en archivos `.log`.
* [ ] Sistema de reintentos configurable.
* [ ] Configuración mediante archivo externo.
* [ ] Detección de cambios en canciones ya descargadas.
* [ ] Interfaz gráfica.
* [ ] Generación de diferentes formatos de salida.
* [ ] Estadísticas más detalladas de la biblioteca.
* [ ] Mejor gestión de versiones modificadas en el sitio.

---

# 🎯 Objetivo del proyecto

El objetivo de **Biblioteca LaCuerda** es automatizar una tarea repetitiva: transformar listas de canciones disponibles en LaCuerda en una biblioteca local organizada, manteniendo separadas las diferentes versiones y tipos de transcripción.

El flujo general es:

```text
                    lista.html
                        │
                        ▼
                Detectar artista
                        │
                        ▼
                Generar posibles
                    URLs
                        │
                        ▼
                Validar ruta
                        │
                        ▼
                Detectar canciones
                        │
                        ▼
                Detectar versiones
                        │
                        ▼
                 Descargar
                        │
              ┌─────────┴─────────┐
              │                   │
          Correcto           Error temporal
              │                   │
              ▼                   ▼
        Guardar archivo      Reintentar al final
              │
              ▼
       Biblioteca_LaCuerda/
              │
              └── Artista/
                    ├── Canción - Acordes.txt
                    ├── Canción - Tablatura.txt
                    └── Canción - Bajo.txt
```

---

## 📜 Licencia

La licencia del código del proyecto se encuentra determinada por la configuración del repositorio.

El contenido descargado mediante el programa puede estar sujeto a derechos de autor y a las condiciones de uso de LaCuerda.net.

La licencia del código y los derechos sobre las tablaturas, acordes y demás contenido descargado deben considerarse por separado.
