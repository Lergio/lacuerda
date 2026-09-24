# 🎸 Biblioteca LaCuerda

Herramienta en Python para automatizar la creación y actualización de una biblioteca local de **acordes, tablaturas, bajo, armónica y teclado** a partir de listas de canciones de [LaCuerda.net](https://lacuerda.net/).

El proyecto permite analizar un archivo `lista.html`, identificar el artista y sus canciones, detectar las diferentes versiones disponibles y descargar las transcripciones como archivos `.txt` organizados por artista.

A partir de la **versión 4**, el proyecto incorpora una interfaz de menú en consola y separa el lanzador de la lógica principal de procesamiento.

---

# 🚀 Versión 4

La versión 4 introduce una nueva organización del proyecto:

```text
lacuerda_v4.py
       │
       ▼
   Menú principal
       │
       ├── Descargar / actualizar biblioteca
       │
       ├── Verificar lista.html
       │
       ├── Ver estado de descargas
       │
       └── Salir
       │
       ▼
funciones.py
       │
       └── Lógica de procesamiento
```

El archivo `lacuerda_v4.py` funciona como **lanzador** y delega las tareas principales en `funciones.py`.

Esto permite separar la interfaz de usuario de las funciones encargadas del procesamiento.

---

# 📋 Características

## Biblioteca

* 🎤 Detección automática del artista desde `lista.html`.
* ⌨️ Posibilidad de indicar el artista manualmente.
* 🔤 Generación automática del `slug` utilizado por LaCuerda.
* 🌎 Manejo de tildes y caracteres especiales.
* `ñ` convertida al formato utilizado por LaCuerda.
* 🅰️ Tratamiento especial para `El`, `La`, `Los` y `Las` al resolver URLs.
* 🔎 Verificación de la ruta del artista antes de descargar.
* ✏️ Posibilidad de introducir manualmente la ruta correcta.
* 🎵 Detección de canciones desde `lista.html`.
* 🧹 Eliminación de canciones duplicadas.
* 🎼 Detección de múltiples versiones.
* 🎸 Soporte para diferentes tipos de transcripción:

  * Acordes
  * Tablatura
  * Bajo
  * Armónica
  * Teclado
* 📄 Un archivo `.txt` independiente para cada versión.
* 🚫 Evita descargar nuevamente archivos existentes.
* 💾 Escritura atómica de los archivos.
* 🛑 Interrupción segura mediante `Ctrl+C`.
* 🔁 Reintentos de errores de conexión y `timeout`.
* 📊 Resumen de descargas y errores.

## Interfaz

La versión 4 incorpora un menú principal con las siguientes opciones:

```text
========== LaCuerda Downloader ==========
  1) Descargar / actualizar biblioteca (usa el lista.html actual)
  2) Verificar el lista.html actual (sin descargar nada)
  3) Ver estado de descargas de un artista
  4) Salir
==========================================
```

---

# 🖥️ Menú principal

Al ejecutar `lacuerda_v4.py`, se muestra el menú principal.

```bash
python lacuerda_v4.py
```

El programa queda esperando que el usuario seleccione una de las opciones disponibles.

---

## 1. Descargar / actualizar biblioteca

Esta opción ejecuta:

```python
flc.procesar_biblioteca_completa()
```

Utiliza el `lista.html` actual y ejecuta el proceso de descarga o actualización de la biblioteca.

Si ya existen archivos descargados, estos se omiten de acuerdo con la lógica implementada en `funciones.py`.

Esta opción es la equivalente al proceso principal de descarga de las versiones anteriores, pero ahora se accede a ella desde el menú.

---

## 2. Verificar el `lista.html` actual

Esta opción ejecuta:

```python
flc.verificar_lista_html()
```

Permite verificar el archivo `lista.html` **sin iniciar una descarga**.

Esta funcionalidad está pensada para poder revisar el estado o contenido de la lista antes de ejecutar una actualización de la biblioteca.

> El detalle exacto de las comprobaciones realizadas pertenece a `funciones.py`.

---

## 3. Ver estado de descargas de un artista

Esta opción solicita:

```text
Nombre del artista (tal como se guardó la carpeta):
```

Por ejemplo:

```text
Abel Pintos
```

Luego ejecuta:

```python
flc.contar_descargas_artista(nombre_artista)
```

El programa muestra:

```text
📁 Carpeta: ...
🎵 Archivos .txt descargados: ...
```

Esto permite consultar rápidamente cuántos archivos `.txt` existen para un determinado artista.

El nombre debe coincidir con el utilizado para la carpeta de la biblioteca.

---

## 4. Salir

Finaliza el programa:

```text
¡Listo! Hasta la próxima.
```

---

# 📁 Estructura del proyecto

La versión 4 separa el lanzador de las funciones principales.

La estructura esperada es:

```text
scraps_lacuerda/
│
├── lacuerda_v4.py
├── funciones.py
└── lista.html
```

La biblioteca generada se almacena en:

```text
Biblioteca_LaCuerda/
```

Por ejemplo:

```text
scraps_lacuerda/
│
├── lacuerda_v4.py
├── funciones.py
├── lista.html
│
└── Biblioteca_LaCuerda/
    │
    ├── Abel_Pintos/
    │   ├── Cancion 1 - Acordes.txt
    │   ├── Cancion 1 - Tablatura.txt
    │   └── Cancion 2 - Acordes.txt
    │
    └── Attaque_77/
        ├── Cancion 1 - Acordes.txt
        └── Cancion 2 - Tablatura.txt
```

---

# 🧩 Separación de responsabilidades

Una de las principales modificaciones de la versión 4 es la separación entre el programa principal y las funciones.

## `lacuerda_v4.py`

Es el **lanzador**.

Se encarga de:

* Mostrar el banner.
* Mostrar el menú.
* Recibir la opción seleccionada.
* Ejecutar la función correspondiente.
* Volver al menú después de cada operación.
* Finalizar el programa cuando el usuario selecciona salir.

El archivo importa las funciones mediante:

```python
import funciones as flc
```

---

## `funciones.py`

Contiene la lógica real del proyecto.

Entre las funciones utilizadas actualmente por el lanzador se encuentran:

```python
flc.procesar_biblioteca_completa()
flc.verificar_lista_html()
flc.contar_descargas_artista()
flc.instalar_manejador_interrupciones()
```

La separación permite modificar la lógica del descargador sin tener que modificar necesariamente el menú principal.

---

# 🎨 Banner

Al iniciar el programa se muestra un pequeño banner:

```text
░▄▀▀▀▀▄░░▄▄░░░░░░░░░░░
█░░░░░░▀▀░░█░░░░░░▄░▄░
█░║░░░░██░████████████
```

seguido del título:

```text
========== LaCuerda Downloader ==========
```

---

# 🎵 Procesamiento de canciones

El sistema utiliza `lista.html` como fuente de información para identificar las canciones del artista.

El proceso general es:

```text
lista.html
    │
    ▼
Identificación del artista
    │
    ▼
Detección de canciones
    │
    ▼
Resolución de URL
    │
    ▼
Detección de versiones
    │
    ▼
Descarga
    │
    ▼
Archivos .txt
```

La lógica detallada del procesamiento se encuentra en `funciones.py`.

---

# 🎼 Tipos de versiones

El sistema reconoce actualmente los siguientes tipos:

| Código | Tipo      |
| ------ | --------- |
| `R`    | Acordes   |
| `T`    | Tablatura |
| `B`    | Bajo      |
| `H`    | Armónica  |
| `K`    | Teclado   |

Estos códigos son interpretados a partir de la información proporcionada por LaCuerda.

---

# 📄 Archivos generados

Las diferentes versiones de una canción se almacenan como archivos independientes.

Ejemplo:

```text
Biblioteca_LaCuerda/
└── Abel_Pintos/
    ├── La_Llave - Acordes.txt
    ├── La_Llave - Tablatura.txt
    └── La_Llave - Bajo.txt
```

Cuando existen varias versiones del mismo tipo, se utilizan números para evitar sobrescribir archivos:

```text
Cancion - Acordes 1.txt
Cancion - Acordes 2.txt
Cancion - Acordes 3.txt
```

---

# 💾 Seguridad de los archivos

La versión anterior del descargador incorporó escritura atómica para evitar archivos incompletos.

El principio es:

```text
Descarga
   │
   ▼
Archivo temporal .tmp
   │
   ▼
Escritura completa
   │
   ▼
Renombrado al archivo definitivo
```

De esta forma, una interrupción durante la escritura no debería dejar un `.txt` parcialmente escrito que pueda confundirse con una descarga completa.

---

# 🛑 Interrupción segura

El sistema mantiene el manejo de interrupciones incorporado en versiones anteriores.

Al presionar:

```text
Ctrl+C
```

el proceso puede detenerse de forma controlada.

La instalación del manejador se realiza al iniciar el programa:

```python
flc.instalar_manejador_interrupciones()
```

---

# 🔁 Reanudación

Los archivos que ya existen no necesitan descargarse nuevamente.

Esto permite detener el proceso y volver a ejecutar la opción:

```text
1) Descargar / actualizar biblioteca
```

para continuar con el procesamiento.

---

# 🌐 Manejo de errores

El descargador cuenta con mecanismos para manejar errores de conexión, `timeout` y determinados códigos HTTP.

Los errores de conexión transitorios pueden ser reintentados al finalizar el recorrido.

Esto permite que un fallo temporal de red no necesariamente interrumpa toda la descarga.

---

# 🛠️ Requisitos

Se necesita:

* **Python 3.8 o superior**
* `requests`
* `beautifulsoup4`

Instalar las dependencias:

```bash
pip install requests beautifulsoup4
```

---

# 🚀 Instalación

Clonar el repositorio:

```bash
git clone https://github.com/Lergio/scraps_lacuerda.git
```

Entrar en la carpeta:

```bash
cd scraps_lacuerda
```

Instalar las dependencias:

```bash
pip install requests beautifulsoup4
```

Colocar el `lista.html` correspondiente en la carpeta del proyecto.

Finalmente:

```bash
python lacuerda_v4.py
```

---

# 🔒 Uso responsable

Este proyecto automatiza solicitudes hacia un sitio web externo.

Se recomienda:

* Respetar los términos de uso del sitio.
* Respetar `robots.txt` y cualquier restricción aplicable.
* Mantener una frecuencia razonable de solicitudes.
* No eliminar las pausas entre solicitudes sin una razón válida.
* Utilizar el contenido descargado de acuerdo con los derechos de autor correspondientes.
* No redistribuir contenido protegido sin la autorización necesaria.

El proyecto automatiza el procesamiento y organización del contenido; los derechos sobre dicho contenido pertenecen a sus respectivos titulares.

---

# 🚧 Estado del proyecto

La versión 4 representa un paso hacia una estructura más modular.

Hasta la versión anterior, el archivo principal concentraba la lógica del descargador.

A partir de esta versión:

```text
lacuerda_v4.py
```

se utiliza como punto de entrada y menú, mientras que:

```text
funciones.py
```

contiene la lógica de procesamiento.

Esto deja preparado el proyecto para seguir agregando funcionalidades sin concentrar toda la lógica en un único archivo.

---

# 💡 Próximas mejoras

Algunas posibles mejoras:

* [ ] Procesamiento automático de múltiples artistas.
* [ ] Mejoras en la verificación de `lista.html`.
* [ ] Información más detallada sobre el estado de cada artista.
* [ ] Registro de errores en archivos `.log`.
* [ ] Configuración mediante archivo externo.
* [ ] Detección de cambios en canciones ya descargadas.
* [ ] Interfaz gráfica.
* [ ] Generación de índices de canciones.
* [ ] Estadísticas generales de la biblioteca.
* [ ] Sistema de actualización más avanzado.

---

# 🎯 Objetivo del proyecto

El objetivo de **Biblioteca LaCuerda** es convertir el proceso de recopilación y organización de acordes y tablaturas en una tarea automatizada y reutilizable.

La evolución del proyecto busca pasar de un script puntual a una herramienta organizada:

```text
                 LaCuerda Downloader
                         │
                         ▼
                    Menú principal
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
      Descargar       Verificar      Estado
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                    funciones.py
                         │
                         ▼
               Biblioteca_LaCuerda/
                         │
                  ┌──────┴──────┐
                  ▼             ▼
              Artista 1      Artista 2
                  │             │
                  ▼             ▼
               Canciones      Canciones
```

La versión 4 establece así una base más modular para las próximas etapas del proyecto.
