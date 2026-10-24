import socket
from datetime import datetime

# Escaneo local para fines educativos
IP_OBJETIVO = "127.0.0.1"

# Puertos que vamos a comprobar
PUERTOS = {
    80: "HTTP",
    443: "HTTPS",
    5000: "Flask - Aplicacion vulnerable",
    5001: "Flask - Aplicacion segura",
    8000: "Servidor web alternativo",
    8080: "HTTP alternativo"
}


def escanear_puerto(ip, puerto):
    """Comprueba si un puerto acepta conexiones TCP."""

    conexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conexion.settimeout(0.5)

    try:
        resultado = conexion.connect_ex((ip, puerto))

        if resultado == 0:
            return True

        return False

    except socket.error:
        return False

    finally:
        conexion.close()


def ejecutar_escaneo():
    print("=" * 60)
    print("       ESCANEO BASICO DE PUERTOS Y SERVICIOS")
    print("       Materia: Seguridad Informatica")
    print("=" * 60)

    print(f"Equipo objetivo: {IP_OBJETIVO}")
    print(f"Fecha y hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("-" * 60)

    abiertos = 0
    cerrados = 0

    for puerto, servicio in PUERTOS.items():
        if escanear_puerto(IP_OBJETIVO, puerto):
            print(f"[ABIERTO] Puerto {puerto:<5} | {servicio}")
            abiertos += 1
        else:
            print(f"[CERRADO] Puerto {puerto:<5} | {servicio}")
            cerrados += 1

    print("-" * 60)
    print("RESUMEN DEL ESCANEO")
    print(f"Puertos revisados: {len(PUERTOS)}")
    print(f"Puertos abiertos: {abiertos}")
    print(f"Puertos cerrados o sin conexion: {cerrados}")
    print("=" * 60)
    print("Escaneo finalizado.")


if __name__ == "__main__":
    ejecutar_escaneo()
