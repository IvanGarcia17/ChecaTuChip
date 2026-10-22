import hid
import time

VID = 0x1A86
PID = 0xE010

print("Buscando interfaz propietaria del RU5600...")

dispositivos = hid.enumerate(VID, PID)

propietario = None

for d in dispositivos:
    if (
        d.get("interface_number") == 0
        and d.get("usage_page") == 0xFF00
    ):
        propietario = d
        break

if propietario is None:
    print("No se encontró la interfaz propietaria del RU5600.")
    input("\nPresiona ENTER para salir...")
    exit()

print("Interfaz encontrada:")
print(propietario["path"])
print()

lector = hid.device()

try:
    lector.open_path(propietario["path"])

    print("RU5600 conectado correctamente.")
    print()
    print("Acerca UNA etiqueta UHF al lector.")
    print("La prueba durará 10 segundos.")
    print()
    print("Escuchando...")
    print("-" * 70)

    inicio = time.time()
    contador = 0

    while time.time() - inicio < 10:

        datos = lector.read(64, timeout_ms=500)

        if datos:

            contador += 1

            print()
            print(f"LECTURA #{contador}")
            print("-" * 70)

            print("HEX:")
            print(" ".join(f"{x:02X}" for x in datos))

            print()
            print("DEC:")
            print(datos)

            print()
            print("ASCII:")
            print(
                "".join(
                    chr(x) if 32 <= x <= 126 else "."
                    for x in datos
                )
            )

            print("-" * 70)

    print()
    print("=" * 70)
    print(f"Fin de la prueba. Paquetes recibidos: {contador}")
    print("=" * 70)

except KeyboardInterrupt:
    print()
    print("Programa detenido.")

except Exception as e:
    print()
    print("ERROR:")
    print(e)

finally:
    try:
        lector.close()
    except:
        pass

input("\nPresiona ENTER para salir...")