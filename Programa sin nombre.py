import hid
import time
import sys

VID = 0x1A86
PID = 0xE010

print("Buscando interfaz propietaria del RU5600...")

devices = hid.enumerate(VID, PID)

lector_info = None

for d in devices:
    if (
        d.get("interface_number") == 0
        and d.get("usage_page") == 0xFF00
    ):
        lector_info = d
        break

if lector_info is None:
    print("No se encontró el RU5600.")
    input("\nPresiona ENTER para salir...")
    sys.exit()

print("\nInterfaz encontrada:")
print(lector_info["path"])

lector = hid.device()

try:

    lector.open_path(lector_info["path"])

    print("\nRU5600 conectado correctamente.")
    print("\nColoca una etiqueta frente al lector.")
    input("Presiona ENTER para comenzar...")

    # Limpiar posibles datos pendientes
    while True:
        datos = lector.read(64, timeout_ms=10)
        if not datos:
            break

    print("\nEnviando Output Report de prueba...")

    paquete = [0] * 64

    resultado = lector.write(paquete)

    print("write() =", resultado)

    print("\nEscuchando durante 5 segundos...")
    print("=" * 70)

    inicio = time.time()
    contador = 0

    while time.time() - inicio < 5:

        datos = lector.read(64, timeout_ms=100)

        if datos:

            contador += 1

            print(f"\nPAQUETE #{contador}")
            print("Cantidad:", len(datos))

            print(
                "HEX:",
                " ".join(f"{b:02X}" for b in datos)
            )

    print("\n" + "=" * 70)
    print("Paquetes recibidos:", contador)

except Exception as e:

    print("\nERROR:")
    print(type(e).__name__)
    print(str(e))

finally:

    try:
        lector.close()
    except:
        pass

input("\nPresiona ENTER para salir...")