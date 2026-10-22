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
    print("No se encontró la interfaz propietaria.")
    input("\nPresiona ENTER para salir...")
    sys.exit()

print("Interfaz encontrada:")
print(lector_info["path"])
print()

lector = hid.device()

try:
    lector.open_path(lector_info["path"])

    print("RU5600 conectado correctamente.")
    print()
    print("=" * 70)
    print("INFORMACIÓN HID")
    print("=" * 70)

    print("Manufacturer :", lector.get_manufacturer_string())
    print("Product      :", lector.get_product_string())
    print("Serial       :", lector.get_serial_number_string())

    print(f"VID          : 0x{VID:04X}")
    print(f"PID          : 0x{PID:04X}")

    print()
    print("Obteniendo Report Descriptor...")

    descriptor = lector.get_report_descriptor()

    print()
    print("Tamaño del descriptor:", len(descriptor), "bytes")

    print()
    print("=" * 70)
    print("REPORT DESCRIPTOR - HEX")
    print("=" * 70)

    for i in range(0, len(descriptor), 16):
        bloque = descriptor[i:i+16]

        print(
            f"{i:04X}: " +
            " ".join(f"{b:02X}" for b in bloque)
        )

    print()
    print("=" * 70)
    print("REPORT DESCRIPTOR - DECIMAL")
    print("=" * 70)

    print(list(descriptor))

except Exception as e:

    print()
    print("=" * 70)
    print("ERROR")
    print("=" * 70)

    print(type(e).__name__)
    print(str(e))

finally:

    try:
        lector.close()
    except:
        pass

input("\nPresiona ENTER para salir...")