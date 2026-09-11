import os
import re
import sys
import time
import unicodedata
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Mapeo de la letra de tipo (según el atributo lcd) a un nombre legible
TIPOS = {
    "R": "Acordes",
    "T": "Tablatura",
    "B": "Bajo",
    "H": "Armonica",
    "K": "Teclado",
}

# --- Configuración general (esto ya no cambia por artista) ---
CARPETA_PRINCIPAL = "Biblioteca_LaCuerda"
ARCHIVO_HTML_LOCAL = "lista.html"
DOMINIO_BASE = "https://acordes.lacuerda.net"


def slugify_artista(nombre):
    """Convierte 'Abel Pintos' -> 'abel_pintos', sacando tildes/ñ,
    que es el formato que usa lacuerda.net en sus URLs.

    Caso particular: lacuerda.net no reemplaza la 'ñ' por 'n' sino por 'ni'
    (ej: 'Chaqueño' -> 'chaquenio', no 'chaqueno'). Por eso la reemplazamos
    explícitamente ANTES de sacar el resto de las tildes con NFKD, porque
    esa normalización la convertiría en una simple 'n'."""
    con_ni = nombre.replace("ñ", "ni").replace("Ñ", "Ni")
    sin_tildes = unicodedata.normalize("NFKD", con_ni)
    sin_tildes = "".join(c for c in sin_tildes if not unicodedata.combining(c))
    slug = sin_tildes.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    slug = slug.strip("_")
    return slug


# Artículos iniciales que lacuerda.net suele omitir al armar la URL
# del artista (ej: "Los Pericos" -> lacuerda.net/pericos/, no /los_pericos/)
ARTICULOS_INICIALES = ("el", "la", "los", "las")


def quitar_articulo_inicial(nombre):
    """Si el nombre del artista empieza con un artículo (El/La/Los/Las),
    devuelve el nombre sin ese artículo. Si no aplica, devuelve None."""
    partes = nombre.strip().split(" ", 1)
    if len(partes) < 2:
        return None
    primera_palabra, resto = partes
    if primera_palabra.lower() in ARTICULOS_INICIALES:
        return resto.strip()
    return None


def generar_candidatos_slug(nombre):
    """Genera la lista de slugs candidatos para el nombre del artista,
    en orden de prioridad: primero el slug 'completo', y si el nombre
    empieza con un artículo (El/La/Los/Las), también el slug sin ese
    artículo, ya que lacuerda.net suele omitirlo en la URL."""
    candidatos = [slugify_artista(nombre)]

    nombre_sin_articulo = quitar_articulo_inicial(nombre)
    if nombre_sin_articulo:
        slug_sin_articulo = slugify_artista(nombre_sin_articulo)
        if slug_sin_articulo not in candidatos:
            candidatos.append(slug_sin_articulo)

    return candidatos


def extraer_nombre_artista(html_contenido):
    """Busca <script>bName='Andrés Calamaro'</script> (o similar) en el HTML
    y devuelve el nombre del artista, o None si no lo encuentra."""
    match = re.search(r"bName\s*=\s*['\"]([^'\"]+)['\"]", html_contenido)
    if match:
        return match.group(1).strip()
    return None


def pedir_datos_artista(html_contenido):
    """Obtiene el nombre del artista: primero intenta detectarlo automáticamente
    desde el propio lista.html (bName=...); si no lo encuentra, usa el argumento
    de consola o lo pregunta por input. Deriva el slug de URL a partir del nombre."""
    nombre = extraer_nombre_artista(html_contenido)

    if nombre:
        print(f"🎤 Artista detectado automáticamente en el HTML: '{nombre}'")
    elif len(sys.argv) > 1:
        nombre = " ".join(sys.argv[1:]).strip()
    else:
        nombre = input(
            "No se encontró 'bName' en lista.html. "
            "¿Nombre del artista (tal como querés que se llame la carpeta)? "
        ).strip()

    if not nombre:
        print("❌ No se pudo determinar el nombre del artista. Abortando.")
        sys.exit(1)

    candidatos_slug = generar_candidatos_slug(nombre)
    if len(candidatos_slug) > 1:
        print(f"🌐 Slugs de URL candidatos (se probarán en orden): {candidatos_slug}")
    else:
        print(f"🌐 Slug de URL derivado: '{candidatos_slug[0]}'")

    return nombre, candidatos_slug


def parsear_versiones(lcd, slug, ruta_artista_url):
    """
    A partir del atributo lcd (ej: 'RRTKT-12534') y el slug de la canción,
    devuelve una lista de tuplas (tipo_legible, url, sufijo) para cada versión.

    El lcd tiene el formato "<letras>-<numeros>", donde cada posición i
    empareja letras[i] (tipo de transcripción) con numeros[i] (el sufijo
    que se usa en la URL: 1 = sin sufijo, 2 = "-2", 3 = "-3", etc).
    """
    versiones = []
    if not lcd or "-" not in lcd:
        # Formato inesperado: como fallback, asumimos una sola versión (acordes)
        return [("Acordes", f"{DOMINIO_BASE}/{ruta_artista_url}/{slug}.shtml", 1)]

    letras, numeros = lcd.split("-", 1)
    if len(letras) != len(numeros):
        # No matchea 1 a 1, usamos fallback simple
        return [("Acordes", f"{DOMINIO_BASE}/{ruta_artista_url}/{slug}.shtml", 1)]

    for letra, num in zip(letras, numeros):
        try:
            sufijo = int(num)
        except ValueError:
            continue
        tipo = TIPOS.get(letra, letra)  # si aparece una letra nueva, se usa tal cual
        sufijo_url = "" if sufijo == 1 else f"-{sufijo}"
        url = f"{DOMINIO_BASE}/{ruta_artista_url}/{slug}{sufijo_url}.shtml"
        versiones.append((tipo, url, sufijo))

    # Ordenamos por sufijo para que el nombre de archivo sea consistente
    versiones.sort(key=lambda v: v[2])
    return versiones


def nombre_seguro(texto):
    limpio = "".join(c for c in texto if c.isalnum() or c in (" ", "_", "-")).strip()
    return re.sub(r"\s+", " ", limpio)


def pedir_slug_manual(ruta_artista_url_actual):
    """Le pide al usuario el tramo final de la URL del artista
    (ej: 'bersuit' para https://acordes.lacuerda.net/bersuit/)."""
    print(f"   URL probada: {DOMINIO_BASE}/{ruta_artista_url_actual}/ -> no existe (404)")
    nuevo = input(
        "   Ingresá manualmente el tramo de URL correcto del artista "
        "(la parte entre lacuerda.net/ y la siguiente barra, ej: 'bersuit'): "
    ).strip().strip("/")
    return nuevo


def probar_ruta_artista(ruta_candidata, slug_primera_cancion):
    """Prueba una única ruta de artista contra la primera canción de la
    lista. Devuelve True si responde 200, False en cualquier otro caso
    (404, otro código, o fallo de conexión)."""
    url_prueba = f"{DOMINIO_BASE}/{ruta_candidata}/{slug_primera_cancion}.shtml"
    print(f"🔎 Verificando ruta de artista con: {url_prueba}")
    try:
        resp = requests.get(url_prueba, headers=HEADERS, timeout=15)
    except Exception as e:
        print(f"   ❌ Fallo de conexión al verificar: {e}")
        return False

    if resp.status_code == 200:
        print(f"   ✅ Ruta de artista válida: '{ruta_candidata}'")
        return True

    print(f"   ⚠️ La ruta '{ruta_candidata}' no funcionó (código: {resp.status_code}).")
    return False


def resolver_ruta_artista(candidatos_slug, slug_primera_cancion):
    """Recibe la lista de rutas candidatas para el artista (ej: el slug
    completo y, si aplica, el slug sin el artículo inicial El/La/Los/Las)
    y las prueba en orden contra la primera canción de la lista.

    Si ninguna funciona, corta el recorrido, pide por teclado el tramo
    correcto de la URL y reintenta hasta encontrar una ruta válida (o
    hasta que el usuario cancele)."""
    for candidato in candidatos_slug:
        if probar_ruta_artista(candidato, slug_primera_cancion):
            return candidato

    # Ninguno de los candidatos automáticos funcionó: pedimos manualmente
    ruta_actual = candidatos_slug[-1]
    while True:
        nuevo = pedir_slug_manual(ruta_actual)
        if not nuevo:
            print("   ❌ No se ingresó ninguna ruta. Abortando.")
            sys.exit(1)

        if probar_ruta_artista(nuevo, slug_primera_cancion):
            return nuevo

        ruta_actual = nuevo
        print(f"   🔁 Reintentando el recorrido de {ARCHIVO_HTML_LOCAL} con la nueva ruta: '{ruta_actual}'")


def procesar_biblioteca_completa():
    print("--- INICIANDO SCRIPT (con soporte multi-versión) ---")

    if not os.path.exists(ARCHIVO_HTML_LOCAL):
        print(f"❌ Error: No se encuentra el archivo '{ARCHIVO_HTML_LOCAL}' en esta carpeta.")
        return

    with open(ARCHIVO_HTML_LOCAL, "r", encoding="utf-8") as f:
        html_contenido = f.read()

    nombre_artista, candidatos_slug = pedir_datos_artista(html_contenido)

    ruta_carpeta = os.path.join(CARPETA_PRINCIPAL, nombre_artista.replace(" ", "_"))
    os.makedirs(ruta_carpeta, exist_ok=True)
    print(f"📁 Carpeta de destino: {ruta_carpeta}")

    soup = BeautifulSoup(html_contenido, "html.parser")
    elementos_lista = soup.find_all("li")

    # slug -> (titulo, lcd)  -> deduplicado, porque a veces el sitio
    # repite el mismo href en dos <li> distintos con títulos ligeramente distintos
    canciones = {}
    for li in elementos_lista:
        enlace = li.find("a")
        if not enlace:
            continue
        slug = enlace.get("href", "").strip()
        if not slug:
            continue
        # El texto del <a> incluye "acordes"/"tablatura" dentro de un <em>; lo quitamos
        em = enlace.find("em")
        texto_titulo = enlace.text.strip()
        if em:
            texto_titulo = texto_titulo.replace(em.text.strip(), "").strip()

        lcd = li.get("lcd", "")

        if slug not in canciones:
            canciones[slug] = (texto_titulo, lcd)

    print(f"¡Éxito! Se identificaron {len(canciones)} canciones únicas.")

    if not canciones:
        print("❌ No se encontraron canciones en el lista.html. Abortando.")
        return

    # --- Validamos que la ruta de artista sea correcta antes de lanzar la ---
    # descarga masiva. Probamos en orden los slugs candidatos (el completo y,
    # si aplica, el slug sin el artículo inicial El/La/Los/Las) contra la
    # primera canción de la lista; si ninguno funciona, pedimos el tramo de
    # URL correcto por teclado.
    primer_slug = next(iter(canciones))
    ruta_artista_url = resolver_ruta_artista(candidatos_slug, primer_slug)
    print(f"🌐 URLs se armarán como: {DOMINIO_BASE}/{ruta_artista_url}/<cancion>.shtml")

    descargar_canciones(canciones, ruta_artista_url, ruta_carpeta, nombre_artista)


def descargar_canciones(canciones, ruta_artista_url, ruta_carpeta, nombre_artista):
    """Recorre las canciones y descarga cada versión. Si detecta un 404 en el
    primer intento real de descarga (posible indicio de que la ruta de
    artista sigue siendo incorrecta pese a la validación previa), corta el
    recorrido, pide el tramo de URL correcto por teclado y reinicia todo
    el recorrido de lista.html con la ruta corregida."""
    total_versiones_descargadas = 0
    total_versiones_omitidas = 0
    intentos_reales = 0

    for i, (slug, (titulo, lcd)) in enumerate(canciones.items(), start=1):
        versiones = parsear_versiones(lcd, slug, ruta_artista_url)
        base_nombre = nombre_seguro(titulo)

        # Si hay más de una versión del mismo tipo (ej: dos "Acordes"),
        # les agregamos un contador para no pisarse entre archivos
        conteo_tipos = {}
        for tipo, _, _ in versiones:
            conteo_tipos[tipo] = conteo_tipos.get(tipo, 0) + 1

        contador_actual = {}

        print(f"[{i}/{len(canciones)}] {titulo}  ({len(versiones)} versión/es: {[t for t,_,_ in versiones]})")

        for tipo, url_version, sufijo in versiones:
            if conteo_tipos[tipo] > 1:
                contador_actual[tipo] = contador_actual.get(tipo, 0) + 1
                etiqueta = f"{tipo} {contador_actual[tipo]}"
            else:
                etiqueta = tipo

            nombre_archivo = f"{base_nombre} - {etiqueta}.txt"
            ruta_final_txt = os.path.join(ruta_carpeta, nombre_archivo)

            if os.path.exists(ruta_final_txt):
                total_versiones_omitidas += 1
                continue

            print(f"      🔗 [{tipo}] {url_version}")
            time.sleep(2)

            try:
                res_tab = requests.get(url_version, headers=HEADERS, timeout=15)

                if res_tab.status_code == 404 and intentos_reales == 0:
                    # Primer intento real de descarga y da 404: cortamos el
                    # recorrido, pedimos la ruta correcta y reiniciamos todo
                    # el recorrido de lista.html desde cero con esa ruta.
                    print("         ⚠️ 404 en el primer intento real. La ruta de artista sigue mal.")
                    nueva_ruta = pedir_slug_manual(ruta_artista_url)
                    if not nueva_ruta:
                        print("         ❌ No se ingresó ninguna ruta. Abortando.")
                        sys.exit(1)
                    print(f"         🔁 Reiniciando el recorrido de {ARCHIVO_HTML_LOCAL} con la ruta '{nueva_ruta}'...")
                    return descargar_canciones(canciones, nueva_ruta, ruta_carpeta, nombre_artista)

                intentos_reales += 1

                if res_tab.status_code == 200:
                    soup_cancion = BeautifulSoup(res_tab.text, "html.parser")
                    
                    # 1. Buscamos el div principal. 
                    # Pasamos una lista con "tbody" y "t_body" para cubrir cualquier variante en la web
                    div_contenedor = soup_cancion.find("div", id=["tbody", "t_body"])
                    
                    # 2. Buscamos el <pre> dentro de ese div. 
                    # Si la web no tuviera el div por alguna razón, hacemos un fallback buscando cualquier <pre>
                    if div_contenedor:
                        bloque_tablatura = div_contenedor.find("pre")
                    else:
                        bloque_tablatura = soup_cancion.find("pre")

                    # 3. Verificamos que se haya encontrado y que contenga texto real
                    if bloque_tablatura and bloque_tablatura.text.strip():
                        
                        # Al usar .text, BeautifulSoup descarta las etiquetas <div> y <a> internas,
                        # pero mantiene intactos los espacios y la alineación de los acordes.
                        texto_tablatura = bloque_tablatura.text
                        
                        with open(ruta_final_txt, "w", encoding="utf-8") as archivo:
                            archivo.write(f"ARTISTA: {nombre_artista}\n")
                            archivo.write(f"CANCION: {titulo}\n")
                            archivo.write(f"VERSION: {etiqueta}\n")
                            archivo.write(f"URL: {url_version}\n")
                            archivo.write("=" * 40 + "\n\n")
                            archivo.write(texto_tablatura)
                            
                        print(f"         ✅ ¡Descargada! -> {nombre_archivo}")
                        total_versiones_descargadas += 1
                    else:
                        print(f"         ⚠️ No se encontró el texto de la canción en {url_version}")
                else:
                    print(f"         ⚠️ Servidor rechazó la versión (Código {res_tab.status_code}) -> {url_version}")
            except Exception as e:
                print(f"         ❌ Fallo de conexión: {e}")

    print("\n--- RESUMEN ---")
    print(f"Versiones descargadas: {total_versiones_descargadas}")
    print(f"Versiones omitidas (ya existían): {total_versiones_omitidas}")


if __name__ == "__main__":
    procesar_biblioteca_completa()
