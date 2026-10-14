"""
lacuerda.py
--------------
Lanzador del crawler + descargador de LaCuerda v5.2.
"""

import sys
import funciones as flc

BANNER = r"""
╔══════════════════════════════════════════════════╗
║              Biblioteca LaCuerda v5.2            ║
║     Índices → Artistas → Canciones → TXT         ║
╚══════════════════════════════════════════════════╝
"""

OPCIONES = {
    "1": "Scrapear una letra y descargar",
    "2": "Verificar una letra + primer artista",
    "3": "Mostrar estado de una letra",
    "4": "Salir",
}


def mostrar_menu():
    print(BANNER)
    for clave, descripcion in OPCIONES.items():
        print(f"  {clave}) {descripcion}")
    print("=" * 52)


def main():
    flc.instalar_manejador_interrupciones()

    while True:
        mostrar_menu()
        eleccion = input("Elegí una opción: ").strip()

        if eleccion == "1":
            flc.procesar_letra()
        elif eleccion == "2":
            flc.verificar_indice_a()
        elif eleccion == "3":
            flc.mostrar_estado()
        elif eleccion == "4":
            print("¡Listo! Hasta la próxima.")
            sys.exit(0)
        else:
            print("⚠️ Opción inválida, probá de nuevo.")

        input("\n(Presioná Enter para volver al menú)")


if __name__ == "__main__":
    main()
