import hid
import time

VID = 0x1A86
PID = 0xE010

print("Buscando interfaz propietaria del RU5600...")

devices = hid.enumerate(VID, PID)

propietario = None

for d in devices:
    if (
        d.get("interface_number") == 0
        and d.get("usage_page") == 0xFF00
    ):
        propietario = d
        break

if propietario is None:
    print("No se encontró la interfaz propietaria.")
    input("Presiona ENTER para salir...")
    exit()

print("\nInterfaz encontrada:")
print(propietario["path"])

lector = hid.device()
lector.open_path(propietario["path"])

print("\nRU5600 conectado correctamente.")
print()
print("Coloca una etiqueta frente al lector.")
print("Esperando paquetes...")
print("=" * 70)

contador = 0
inicio = time.time()

try:

    while time.time() - inicio < 10:

        datos = lector.read(64, timeout_ms=500)

        if datos:

            contador += 1

            print(f"\nPAQUETE #{contador}")
            print("Cantidad de bytes:", len(datos))

            print("HEX:")
            print(" ".join(f"{b:02X}" for b in datos))

            print("")

except KeyboardInterrupt:
    pass

finally:
    lector.close()

print()
print("=" * 70)
print(f"TOTAL DE PAQUETES: {contador}")
print("=" * 70)

input("Presiona ENTER para salir...")