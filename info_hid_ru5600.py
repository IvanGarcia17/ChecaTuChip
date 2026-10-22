import hid

VID = 0x1A86
PID = 0xE010

print("Buscando RU5600...")
print()

devices = hid.enumerate(VID, PID)

if not devices:
    print("No se encontró el RU5600.")
    input("\nPresiona ENTER para salir...")
    exit()

for i, d in enumerate(devices, 1):

    print("=" * 70)
    print(f"DISPOSITIVO {i}")
    print("=" * 70)

    print("Path:          ", d.get("path"))
    print("VID:           ", f"{d.get('vendor_id'):04X}")
    print("PID:           ", f"{d.get('product_id'):04X}")
    print("Fabricante:    ", d.get("manufacturer_string"))
    print("Producto:      ", d.get("product_string"))
    print("Serial:        ", d.get("serial_number"))
    print("Interfaz:      ", d.get("interface_number"))
    print("Uso:           ", d.get("usage"))
    print("Uso página:    ", d.get("usage_page"))

    print()

input("\nPresiona ENTER para salir...")