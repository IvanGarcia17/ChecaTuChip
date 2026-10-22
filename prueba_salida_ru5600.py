import hid
import sys

VID = 0x1A86
PID = 0xE010

print("Buscando interfaz propietaria del RU5600...\n")

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

print("Interfaz encontrada:")
print(lector_info["path"])

lector = hid.device()

try:

    lector.open_path(lector_info["path"])

    print("\nRU5600 conectado correctamente.")

    paquete = bytes(64)

    print("\nEnviando Output Report de 64 bytes...")
    print("HEX:")
    print(" ".join(f"{b:02X}" for b in paquete))

    resultado = lector.write(paquete)

    print("\nResultado de write():", resultado)

    if resultado == 64:
        print("El Output Report fue enviado correctamente.")
    else:
        print("El lector reportó una cantidad diferente de bytes.")

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