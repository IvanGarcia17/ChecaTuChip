import hid
import time

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
print("Coloca UNA etiqueta frente al lector.")
print("Se tomarán 20 paquetes.")
print()

paquetes = []

while len(paquetes) < 20:

    datos = lector.read(64, timeout_ms=1000)

    if datos:
        paquetes.append(datos)

lector.close()

print()
print("=" * 70)
print("PAQUETES RECIBIDOS:", len(paquetes))
print("=" * 70)

# Buscar qué posiciones cambian
cambiantes = []

for posicion in range(64):

    valores = set()

    for paquete in paquetes:
        valores.add(paquete[posicion])

    if len(valores) > 1:
        cambiantes.append((posicion, valores))

print()
print("POSICIONES QUE CAMBIAN ENTRE LECTURAS:")
print()

if not cambiantes:
    print("Ninguna posición cambia.")
else:
    for posicion, valores in cambiantes:
        valores_hex = " ".join(f"{v:02X}" for v in sorted(valores))

        print(
            f"Byte {posicion:02d}: {valores_hex}"
        )

print()
print("=" * 70)

input("Presiona ENTER para salir...")