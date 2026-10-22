import hid

VID = 0x1A86
PID = 0xE010

print("Buscando RU5600...")

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
    print("No se encontró el RU5600.")
    input("Presiona ENTER para salir...")
    exit()

lector = hid.device()
lector.open_path(propietario["path"])

print("RU5600 conectado.")
print()
print("Acerca una etiqueta...")
print()

while True:

    datos = lector.read(64, timeout_ms=1000)

    if datos:

        byte21 = datos[21]
        byte22 = datos[22]

        identificador = (byte21 << 8) | byte22

        print("=" * 50)
        print("LECTURA RFID")
        print("=" * 50)

        print(f"Byte 21:       {byte21:02X}")
        print(f"Byte 22:       {byte22:02X}")
        print()
        print(f"ID hexadecimal: {byte21:02X}{byte22:02X}")
        print(f"ID decimal:     {identificador}")

        print()