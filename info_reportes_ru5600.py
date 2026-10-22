import hid

VID = 0x1A86
PID = 0xE010

print("Buscando RU5600...")

devices = hid.enumerate(VID, PID)

for d in devices:

    if (
        d.get("interface_number") == 0
        and d.get("usage_page") == 0xFF00
    ):

        print("\nINTERFAZ PROPIETARIA ENCONTRADA")
        print("=" * 70)

        print("Path:")
        print(d["path"])

        print("\nInformación disponible:")
        for clave, valor in d.items():
            print(f"{clave}: {valor}")

        break

else:
    print("No se encontró la interfaz propietaria del RU5600.")

input("\nPresiona ENTER para salir...")