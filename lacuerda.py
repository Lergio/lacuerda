"""
lacuerda_v4.py
--------------
Lanzador del descargador de acordes/tablaturas de lacuerda.net.
Muestra un menú y delega el trabajo real a las funciones de funciones_lc.py.
"""

import sys

import funciones as flc

BANNER = r"""
░▄▀▀▀▀▄░░▄▄░░░░░░░░░░░
█░░░░░░▀▀░░█░░░░░░▄░▄░
█░║░░░░██░████████████
"""

OPCIONES = {
    "1": "Descargar / actualizar biblioteca (usa el lista.html actual)",
    "2": "Verificar el lista.html actual (sin descargar nada)",
    "3": "Ver estado de descargas de un artista",
    "4": "Salir",
}


def mostrar_menu():
    print(BANNER)
    print("========== LaCuerda Downloader ==========")
    for clave, descripcion in OPCIONES.items():
        print(f"  {clave}) {descripcion}")
    print("==========================================")


def opcion_descargar():
    flc.procesar_biblioteca_completa()


def opcion_verificar():
    flc.verificar_lista_html()


def opcion_ver_estado():
    nombre_artista = input("Nombre del artista (tal como se guardó la carpeta): ").strip()
    if not nombre_artista:
        print("❌ No se ingresó ningún nombre.")
        return
    cantidad, ruta_carpeta = flc.contar_descargas_artista(nombre_artista)
    print(f"📁 Carpeta: {ruta_carpeta}")
    print(f"🎵 Archivos .txt descargados: {cantidad}")


def main():
    flc.instalar_manejador_interrupciones()

    while True:
        mostrar_menu()
        eleccion = input("Elegí una opción: ").strip()

        if eleccion == "1":
            opcion_descargar()
        elif eleccion == "2":
            opcion_verificar()
        elif eleccion == "3":
            opcion_ver_estado()
        elif eleccion == "4":
            print("¡Listo! Hasta la próxima.")
            sys.exit(0)
        else:
            print("⚠️ Opción inválida, probá de nuevo.")

        input("\n(Presioná Enter para volver al menú)")


if __name__ == "__main__":
    main()
