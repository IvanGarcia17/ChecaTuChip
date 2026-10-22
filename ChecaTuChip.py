import serial
import serial.tools.list_ports
import time
import csv
import PySimpleGUI as sg
from datetime import datetime

# ===============================
#  CONFIGURACIÓN DEL LECTOR
# ===============================
BAUD = 115200
TIMEOUT = 0.5

# ===============================
#  FUNCIONES PRINCIPALES
# ===============================

def listar_puertos():
    """Devuelve una lista de puertos COM disponibles"""
    return [p.device for p in serial.tools.list_ports.comports()]

def conectar_lector(puerto):
    """Intenta abrir el puerto serial"""
    try:
        ser = serial.Serial(puerto, BAUD, timeout=TIMEOUT)
        return ser
    except Exception as e:
        sg.popup_error(f"No se pudo abrir {puerto}: {e}")
        return None

def enviar_comando(ser, comando_bytes):
    """Envía bytes al lector y devuelve la respuesta cruda"""
    ser.write(comando_bytes)
    time.sleep(0.1)
    data = ser.read(ser.in_waiting or 64)
    return data

def leer_tags_simulado():
    """Simula lectura de etiquetas (para pruebas sin lector)"""
    import random
    tag = f"E200{random.randint(1000000000, 9999999999)}"
    return tag

def leer_tags(ser):
    """
    Envia comando de inventario al lector y devuelve EPCs detectados.
    Nota: este comando depende del protocolo real del RU-5600.
    """
    # Ejemplo genérico de comando (debes reemplazar según manual)
    comando = bytes([0xA0, 0x04, 0x01, 0x00, 0xAB])  # placeholder
    resp = enviar_comando(ser, comando)
    if not resp:
        return []
    # Parsear respuesta (placeholder)
    return [resp.hex()]

def guardar_csv(lista_tags, filename="lecturas.csv"):
    """Guarda los EPC en un CSV"""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Fecha", "EPC"])
        for epc in lista_tags:
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), epc])

# ===============================
#  INTERFAZ GRÁFICA
# ===============================

def main():
    sg.theme("DarkBlue3")

    layout = [
        [sg.Text("Puerto COM:"), sg.Combo(listar_puertos(), key="-COM-", size=(10,1)), 
         sg.Button("Conectar", key="-CONECTAR-"), sg.Button("Actualizar puertos")],
        [sg.Multiline(size=(50,15), key="-SALIDA-", disabled=True)],
        [sg.Button("Leer etiquetas"), sg.Button("Guardar CSV"), sg.Exit()]
    ]

    window = sg.Window("Lector UHF YanPoDo RU-5600", layout)
    ser = None
    lista_tags = []

    while True:
        event, values = window.read(timeout=100)
        if event in (sg.WIN_CLOSED, "Exit"):
            break

        if event == "Actualizar puertos":
            window["-COM-"].update(values=listar_puertos())

        elif event == "-CONECTAR-":
            puerto = values["-COM-"]
            if not puerto:
                sg.popup_error("Selecciona un puerto COM")
                continue
            ser = conectar_lector(puerto)
            if ser:
                sg.popup("Conectado correctamente")
            else:
                sg.popup_error("No se pudo conectar")

        elif event == "Leer etiquetas":
            if ser:
                tags = leer_tags(ser)
            else:
                tags = [leer_tags_simulado()]  # modo demo

            for t in tags:
                if t not in lista_tags:
                    lista_tags.append(t)
                    window["-SALIDA-"].update(f"{t}\n", append=True)

        elif event == "Guardar CSV":
            if lista_tags:
                guardar_csv(lista_tags)
                sg.popup("Archivo guardado como lecturas.csv")
            else:
                sg.popup_error("No hay lecturas para guardar")

    if ser and ser.is_open:
        ser.close()
    window.close()

if __name__ == "__main__":
    main()