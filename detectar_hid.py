import hid

VID = 0x1A86
PID = 0xE010

print("Buscando RU5600...")
print()

dispositivos = hid.enumerate(VID, PID)

if not dispositivos:
    print("No se encontró el RU5600.")
    exit()

print(f"Se encontraron {len(dispositivos)} interfaces.")
print("=" * 70)

for i, d in enumerate(dispositivos, 1):
    print(f"INTERFAZ {i}")
    print(f"  Path:        {d.get('path')}")
    print(f"  VID:         {d.get('vendor_id'):04X}")
    print(f"  PID:         {d.get('product_id'):04X}")
    print(f"  Fabricante:  {d.get('manufacturer_string')}")
    print(f"  Producto:    {d.get('product_string')}")
    print(f"  Serial:      {d.get('serial_number')}")
    print(f"  Uso:         {d.get('usage')}")
    print(f"  Uso página:  {d.get('usage_page')}")
    print(f"  Interfaz:    {d.get('interface_number')}")
    print("-" * 70)