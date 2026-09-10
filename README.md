<html>
<body>
<!--StartFragment--><html><head></head><body><h1>🎸 Biblioteca LaCuerda — Descargador de Tablaturas</h1><p>Script en Python para crear automáticamente una biblioteca local de canciones de un artista a partir de un archivo HTML con enlaces de <strong>LaCuerda.net</strong>.</p><p>El programa analiza un archivo <code inline="">lista.html</code>, identifica las canciones disponibles, visita cada enlace y guarda el contenido de las tablaturas/acordes en archivos <code inline="">.txt</code> organizados por artista.</p><blockquote><p><strong>Nota:</strong> Este proyecto está pensado para uso personal. Respeta los términos de uso, derechos de autor y condiciones del sitio web del que obtengas el contenido.</p></blockquote><hr><h2>📋 ¿Qué hace?</h2><p>El script realiza automáticamente las siguientes tareas:</p><ol><li><p>Busca el archivo <code inline="">lista.html</code> en la carpeta del proyecto.</p></li><li><p>Analiza todos los elementos <code inline="">&lt;li&gt;</code> que contienen enlaces.</p></li><li><p>Obtiene:</p><ul><li><p>El título de la canción.</p></li><li><p>La URL correspondiente en <code inline="">lacuerda.net</code>.</p></li></ul></li><li><p>Elimina de los títulos las palabras <code inline="">acordes</code> y <code inline="">tablatura</code>.</p></li><li><p>Evita procesar canciones duplicadas.</p></li><li><p>Crea automáticamente la carpeta del artista.</p></li><li><p>Visita cada página de canción.</p></li><li><p>Extrae el contenido de la tablatura.</p></li><li><p>Guarda cada canción como un archivo <code inline="">.txt</code>.</p></li><li><p>Salta automáticamente las canciones que ya fueron descargadas.</p></li><li><p>Muestra en consola el progreso de todo el proceso.</p></li></ol><hr><h2>📁 Estructura del proyecto</h2><p>La estructura mínima necesaria es:</p><pre><code class="language-text">Proyecto/
│
├── procesador.py
├── lista.html
└── Biblioteca_LaCuerda/
</code></pre><p>La carpeta <code inline="">Biblioteca_LaCuerda</code> se crea automáticamente si no existe.</p><p>Después de ejecutar el programa, la estructura será similar a:</p><pre><code class="language-text">Proyecto/
│
├── procesador.py
├── lista.html
│
└── Biblioteca_LaCuerda/
    └── Abel_Pintos/
        ├── Aventura.txt
        ├── Cada_Noche.txt
        ├── De_Mi_Algo.txt
        ├── La_Llave.txt
        └── ...
</code></pre><p>El nombre del artista se utiliza para crear automáticamente la carpeta correspondiente, reemplazando los espacios por <code inline="">_</code>.</p><hr><h2>🛠️ Requisitos</h2><p>Se necesita:</p><ul><li><p><strong>Python 3.8 o superior</strong></p></li><li><p><code inline="">requests</code></p></li><li><p><code inline="">beautifulsoup4</code></p></li></ul><p>Las librerías pueden instalarse mediante:</p><pre><code class="language-bash">pip install requests beautifulsoup4
</code></pre><p>O, si utilizas <code inline="">pip3</code>:</p><pre><code class="language-bash">pip3 install requests beautifulsoup4
</code></pre><hr><h2>🚀 Instalación</h2><h3>1. Clonar o descargar el proyecto</h3><p>Coloca el script y el archivo <code inline="">lista.html</code> dentro de la misma carpeta.</p><p>Por ejemplo:</p><pre><code class="language-text">MiBiblioteca/
├── procesador.py
└── lista.html
</code></pre><h3>2. Instalar las dependencias</h3><p>Desde una terminal:</p><pre><code class="language-bash">pip install requests beautifulsoup4
</code></pre><h3>3. Ejecutar el script</h3><pre><code class="language-bash">python procesador.py
</code></pre><hr><h2>📄 El archivo <code inline="">lista.html</code></h2><p>El programa espera encontrar un archivo llamado exactamente:</p><pre><code class="language-text">lista.html
</code></pre><p>El archivo debe contener enlaces a las canciones que se desean procesar.</p><p>Por ejemplo:</p><pre><code class="language-html">&lt;ul&gt;
    &lt;li&gt;
        &lt;a href="/Abel_Pintos/La_Llave.phtml"&gt;
            La Llave acordes
        &lt;/a&gt;
    &lt;/li&gt;

    &lt;li&gt;
        &lt;a href="/Abel_Pintos/Aventura.phtml"&gt;
            Aventura tablatura
        &lt;/a&gt;
    &lt;/li&gt;
&lt;/ul&gt;
</code></pre><p>El programa detectará automáticamente los enlaces y construirá las URL completas:</p><pre><code class="language-text">https://lacuerda.net/Abel_Pintos/La_Llave.phtml
</code></pre><hr><h2>⚙️ Configuración del artista</h2><p>Actualmente el artista está definido directamente dentro del código:</p><pre><code class="language-python">nombre_artista = "Abel Pintos"
</code></pre><p>Para utilizar otro artista, simplemente cambia ese valor:</p><pre><code class="language-python">nombre_artista = "Artista Nuevo"
</code></pre><p>Los archivos se guardarán automáticamente en:</p><pre><code class="language-text">Biblioteca_LaCuerda/Artista_Nuevo/
</code></pre><p>Por ejemplo:</p><pre><code class="language-python">nombre_artista = "Attaque 77"
</code></pre><p>generará:</p><pre><code class="language-text">Biblioteca_LaCuerda/
└── Attaque_77/
</code></pre><hr><h2>🔄 Funcionamiento</h2><p>El flujo general del programa es:</p><pre><code class="language-text">                lista.html
                    │
                    ▼
          ┌────────────────────┐
          │ Analizar HTML      │
          └─────────┬──────────┘
                    │
                    ▼
          Buscar enlaces &lt;a&gt;
                    │
                    ▼
        Obtener título + URL
                    │
                    ▼
          Eliminar duplicados
                    │
                    ▼
       ¿El archivo ya existe?
              /           \
            Sí             No
            │              │
            ▼              ▼
          Saltar       Esperar 2 s
                           │
                           ▼
                    Descargar página
                           │
                           ▼
                  Extraer tablatura
                           │
                           ▼
                     Guardar .txt
                           │
                           ▼
                    Siguiente canción
</code></pre><hr><h2>💾 Formato de los archivos generados</h2><p>Cada canción se guarda como un archivo de texto UTF-8.</p><p>Por ejemplo:</p><pre><code class="language-text">ARTISTA: Abel Pintos
CANCION: La Llave
========================================

[contenido de la tablatura]
</code></pre><p>Esto permite que los archivos sean fáciles de leer, editar, buscar o utilizar posteriormente para construir una biblioteca musical más grande.</p><hr><h2>🛡️ Prevención de descargas duplicadas</h2><p>Antes de descargar una canción, el programa comprueba si el archivo ya existe:</p><pre><code class="language-python">if os.path.exists(ruta_final_txt):
    ...
</code></pre><p>Si ya existe, la canción se salta automáticamente.</p><p>Esto permite ejecutar el programa nuevamente sin tener que descargar toda la biblioteca desde cero.</p><p>Por ejemplo:</p><pre><code class="language-text">[1/120] Saltando (Ya existe): La Llave
[2/120] Saltando (Ya existe): Aventura
[3/120] Guardando: [Sin Principio Ni Final]
</code></pre><hr><h2>🌐 Extracción del contenido</h2><p>El programa utiliza <code inline="">BeautifulSoup</code> para analizar el HTML de cada canción.</p><p>Primero intenta encontrar un bloque:</p><pre><code class="language-html">&lt;pre&gt;
</code></pre><p>mediante:</p><pre><code class="language-python">bloque_tablatura = soup_cancion.find('pre')
</code></pre><p>Si no encuentra dicho bloque, utiliza métodos alternativos:</p><pre><code class="language-python">soup_cancion.find(id="t_body")
</code></pre><p>o:</p><pre><code class="language-python">soup_cancion.find(class_="tablatura")
</code></pre><p>y finalmente utiliza el <code inline="">&lt;body&gt;</code> de la página como último recurso.</p><p>Esto permite que el programa sea más tolerante frente a pequeñas diferencias en la estructura HTML de las páginas.</p><hr><h2>⏱️ Espera entre solicitudes</h2><p>Antes de acceder a cada canción se realiza una pausa:</p><pre><code class="language-python">time.sleep(2)
</code></pre><p>Esto significa que el programa espera <strong>2 segundos entre solicitudes</strong>.</p><p>La espera reduce la velocidad de las peticiones y evita realizar cientos de solicitudes consecutivas de manera demasiado agresiva.</p><hr><h2>🔤 Nombres de archivo</h2><p>Los nombres de las canciones se limpian antes de crear el archivo:</p><pre><code class="language-python">nombre_seguro = "".join(
    c for c in titulo
    if c.isalnum() or c in (' ', '_', '-')
).strip()
</code></pre><p>Esto elimina caracteres que podrían causar problemas en los nombres de archivo.</p><p>Por ejemplo:</p><pre><code class="language-text">¿Y cómo es él?
</code></pre><p>podría convertirse en un nombre compatible con el sistema de archivos.</p><hr><h2>📊 Mensajes durante la ejecución</h2><p>El programa informa en la terminal qué está haciendo.</p><p>Ejemplo:</p><pre><code class="language-text">--- Iniciando Procesador Masivo Blindado para: Abel Pintos ---

¡Éxito! El analizador identificó 120 canciones listas en tu archivo.
Iniciando la descarga automática a tu disco duro...

[1/120] Guardando: [La Llave]
      🔗 URL de descarga: https://lacuerda.net/...
     ✅ ¡Descargada con éxito!

[2/120] Saltando (Ya existe): Aventura

[3/120] Guardando: [Sin Principio Ni Final]
      🔗 URL de descarga: https://lacuerda.net/...
     ⚠️ No se pudo extraer texto limpio de la página.

--- ¡Biblioteca completa de Abel Pintos creada perfectamente! ---
</code></pre><hr><h2>⚠️ Manejo de errores</h2><p>El programa contempla diferentes situaciones:</p><h3>No existe <code inline="">lista.html</code></h3><pre><code class="language-text">❌ Error: No se encuentra el archivo 'lista.html'.
</code></pre><h3>El servidor responde con un error</h3><pre><code class="language-text">⚠️ El servidor rechazó la canción (Código 403)
</code></pre><h3>No se encuentra contenido extraíble</h3><pre><code class="language-text">⚠️ No se pudo extraer texto limpio de la página.
</code></pre><h3>Error de conexión</h3><pre><code class="language-text">❌ Fallo de conexión en La Llave: ...
</code></pre><p>Un error en una canción no detiene necesariamente todo el proceso: el programa continúa con las siguientes canciones.</p><hr><h2>🔧 Dependencias</h2>
Librería | Función
-- | --
os | Manejo de carpetas y archivos
time | Pausas entre solicitudes
requests | Descarga de páginas web
BeautifulSoup | Análisis y extracción del HTML

<p><code inline="">os</code> y <code inline="">time</code> forman parte de la biblioteca estándar de Python.</p><p>Las dependencias externas son:</p><pre><code class="language-text">requests
beautifulsoup4
</code></pre><hr><h2>📝 Personalización</h2><p>Las principales variables que pueden modificarse están al comienzo de la función:</p><pre><code class="language-python">carpeta_principal = "Biblioteca_LaCuerda"
nombre_artista = "Abel Pintos"
archivo_html_local = "lista.html"
</code></pre><p>Por ejemplo:</p><pre><code class="language-python">carpeta_principal = "Mi_Cancionero"
nombre_artista = "Attaque 77"
archivo_html_local = "lista.html"
</code></pre><p>El resultado será:</p><pre><code class="language-text">Mi_Cancionero/
└── Attaque_77/
    ├── Cancion_1.txt
    ├── Cancion_2.txt
    └── Cancion_3.txt
</code></pre><hr><h2>🔒 Uso responsable</h2><p>Este script automatiza solicitudes a un sitio web externo. Se recomienda:</p><ul><li><p>Mantener pausas entre solicitudes.</p></li><li><p>No utilizar el programa para generar tráfico excesivo.</p></li><li><p>Respetar <code inline="">robots.txt</code>, términos de servicio y restricciones del sitio.</p></li><li><p>Utilizar los archivos descargados únicamente de acuerdo con los derechos y permisos correspondientes.</p></li><li><p>No redistribuir contenido protegido por derechos de autor sin autorización.</p></li></ul><hr><h2>📜 Licencia</h2><p>Este código puede adaptarse y modificarse para uso personal.</p><p>El contenido obtenido mediante el script puede estar sujeto a derechos de autor y/o a las condiciones de uso del sitio de origen. El código y el contenido descargado deben considerarse por separado.</p><hr><h2>🎵 Próximas mejoras posibles</h2><p>Algunas mejoras que podrían incorporarse en futuras versiones:</p><ul class="contains-task-list"><li class="task-list-item"><p><input type="checkbox" disabled=""> Permitir seleccionar el artista desde la terminal.</p></li><li class="task-list-item"><p><input type="checkbox" disabled=""> Procesar varios artistas automáticamente.</p></li><li class="task-list-item"><p><input type="checkbox" disabled=""> Crear un archivo índice con todas las canciones.</p></li><li class="task-list-item"><p><input type="checkbox" disabled=""> Detectar automáticamente canciones que fallaron.</p></li><li class="task-list-item"><p><input type="checkbox" disabled=""> Reintentar descargas fallidas.</p></li><li class="task-list-item"><p><input type="checkbox" disabled=""> Registrar errores en un archivo <code inline="">.log</code>.</p></li><li class="task-list-item"><p><input type="checkbox" disabled=""> Descargar solamente nuevas canciones al actualizar <code inline="">lista.html</code>.</p></li><li class="task-list-item"><p><input type="checkbox" disabled=""> Ordenar alfabéticamente los archivos.</p></li><li class="task-list-item"><p><input type="checkbox" disabled=""> Generar una biblioteca completa de múltiples artistas.</p></li><li class="task-list-item"><p><input type="checkbox" disabled=""> Exportar las canciones también a Markdown o HTML.</p></li><li class="task-list-item"><p><input type="checkbox" disabled=""> Añadir una interfaz gráfica.</p></li><li class="task-list-item"><p><input type="checkbox" disabled=""> Incorporar un modo de simulación que muestre qué canciones se descargarían sin realizar solicitudes.</p></li></ul><hr><h2>🎸 Ejemplo de resultado final</h2><p>Una biblioteca completa podría quedar organizada de esta manera:</p><pre><code class="language-text">Biblioteca_LaCuerda/
│
├── Abel_Pintos/
│   ├── Aventura.txt
│   ├── Cada_Noche.txt
│   ├── De_Mi_Algo.txt
│   ├── El_Adivino.txt
│   ├── La_Llave.txt
│   └── Sin_Principio_Ni_Final.txt
│
├── Attaque_77/
│   ├── Arrancacorazones.txt
│   ├── Hacelo_Por_Mi.txt
│   └── ...
│
└── Almafuerte/
    ├── A_Vos_Amigo.txt
    └── ...
</code></pre><p>De esta manera, el script funciona como una herramienta sencilla para transformar listas de enlaces de canciones en una <strong>biblioteca local organizada por artista</strong>.</p></body></html><!--EndFragment-->
</body>
</html>
