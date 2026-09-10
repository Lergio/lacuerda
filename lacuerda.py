import os
import time
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def procesar_biblioteca_completa():
    carpeta_principal = "Biblioteca_LaCuerda"
    nombre_artista = "Abel Pintos"
    archivo_html_local = "lista.html"
    
    print(f"--- Iniciando Procesador Masivo Blindado para: {nombre_artista} ---")
    
    if not os.path.exists(archivo_html_local):
        print(f"❌ Error: No se encuentra el archivo '{archivo_html_local}'.")
        return

    ruta_carpeta = os.path.join(carpeta_principal, nombre_artista.replace(" ", "_"))
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
        
    with open(archivo_html_local, "r", encoding="utf-8") as f:
        html_contenido = f.read()
        
    soup = BeautifulSoup(html_contenido, 'html.parser')
    elementos_lista = soup.find_all('li')
    
    canciones_encontradas = []
    for li in elementos_lista:
        enlace = li.find('a')
        if enlace:
            href_slug = enlace.get('href', '').strip()
            texto_enlace = enlace.text.strip()
            
            if href_slug:
                # URL estricta armada por fuera de cualquier reemplazo de texto
                url_limpia_web = "https://lacuerda.net" + href_slug
                titulo_final_txt = texto_enlace.replace("acordes", "").replace("tablatura", "").strip()
                
                if (titulo_final_txt, url_limpia_web) not in canciones_encontradas:
                    canciones_encontradas.append((titulo_final_txt, url_limpia_web))
                
    print(f"¡Éxito! El analizador identificó {len(canciones_encontradas)} canciones listas en tu archivo.")
    print("Iniciando la descarga automática a tu disco duro...\n")
    
    for i, (titulo, url_tab) in enumerate(canciones_encontradas, start=1):
        nombre_seguro = "".join(c for c in titulo if c.isalnum() or c in (' ', '_', '-')).strip()
        nombre_archivo = f"{nombre_seguro}.txt"
        ruta_final_txt = os.path.join(ruta_carpeta, nombre_archivo)
        
        if os.path.exists(ruta_final_txt):
            print(f"[{i}/{len(canciones_encontradas)}] Saltando (Ya existe): {titulo}")
            continue
            
        print(f"[{i}/{len(canciones_encontradas)}] Guardando: [{titulo}]")
        print(f"      🔗 URL de descarga: {url_tab}")
        time.sleep(2)
        
        try:
            res_tab = requests.get(url_tab, headers=HEADERS, timeout=15)
            
            if res_tab.status_code == 200:
                soup_cancion = BeautifulSoup(res_tab.text, 'html.parser')
                bloque_tablatura = soup_cancion.find('pre')
                
                if bloque_tablatura:
                    texto_tablatura = bloque_tablatura.text
                else:
                    bloque_alt = soup_cancion.find(id="t_body") or soup_cancion.find(class_="tablatura") or soup_cancion.body
                    texto_tablatura = bloque_alt.text if bloque_alt else ""
                
                if texto_tablatura:
                    with open(ruta_final_txt, "w", encoding="utf-8") as archivo:
                        archivo.write(f"ARTISTA: {nombre_artista}\n")
                        archivo.write(f"CANCION: {titulo}\n")
                        archivo.write("="*40 + "\n\n")
                        archivo.write(texto_tablatura)
                    print(f"     ✅ ¡Descargada con éxito!")
                else:
                    print(f"     ⚠️ No se pudo extraer texto limpio de la página.")
            else:
                print(f"     ⚠️ El servidor rechazó la canción (Código {res_tab.status_code})")
        except Exception as e:
            print(f"     ❌ Fallo de conexión en {titulo}: {e}")
            
    print(f"\n--- ¡Biblioteca completa de {nombre_artista} creada perfectamente! ---")

if __name__ == "__main__":
    procesar_biblioteca_completa()
