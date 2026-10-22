import usb.core
import usb.util

VID = 0x1A86
PID = 0xE010

print("Buscando RU5600...")

device = usb.core.find(idVendor=VID, idProduct=PID)

if device is None:
    print("RU5600 NO encontrado.")
    print("Verifica que esté conectado.")
    exit()

print("RU5600 encontrado.")
print("=" * 50)

print(f"VID: {device.idVendor:04X}")
print(f"PID: {device.idProduct:04X}")
print()

for cfg in device:
    print(f"Configuración: {cfg.bConfigurationValue}")

    for interface in cfg:
        print(
            f"  Interfaz: {interface.bInterfaceNumber} "
            f"| Clase: {interface.bInterfaceClass} "
            f"| Subclase: {interface.bInterfaceSubClass} "
            f"| Protocolo: {interface.bInterfaceProtocol}"
        )

        for endpoint in interface:
            direccion = "IN" if endpoint.bEndpointAddress & 0x80 else "OUT"

            print(
                f"      Endpoint: 0x{endpoint.bEndpointAddress:02X} "
                f"| {direccion} "
                f"| Tipo: {usb.util.endpoint_type(endpoint.bmAttributes)} "
                f"| Tamaño: {endpoint.wMaxPacketSize}"
            )

print("=" * 50)
print("Detección terminada.")