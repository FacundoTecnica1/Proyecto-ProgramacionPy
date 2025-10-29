import serial
import time

# --- CONFIGURACIÓN ---
PUERTO_SERIAL = 'COM7'  # <-- ¡AJUSTA ESTO A TU PUERTO!
VELOCIDAD_SERIAL = 9600 

def probar_conexion_serial():
    print(f"Intentando conectar a {PUERTO_SERIAL} a {VELOCIDAD_SERIAL} baudios...")
    
    try:
        # Abre la conexión serial
        ser = serial.Serial(PUERTO_SERIAL, VELOCIDAD_SERIAL, timeout=0.1)
        print("✅ Conexión establecida. Presiona el botón de Arduino...")
        print("Presiona Ctrl+C para salir.")
        
        while True:
            # Lee todos los datos disponibles en el buffer
            data = ser.read_all()
            
            if data:
                # Si recibimos datos, los decodificamos (de bytes a texto) y los mostramos
                data_str = data.decode('utf-8', errors='ignore').strip()
                
                # Buscamos la señal 'S'
                if 'S' in data_str:
                    print(f"🤖 Señal de salto recibida: {data_str}")
            
            time.sleep(0.01) # Pequeña pausa para no saturar el CPU

    except serial.SerialException as e:
        print(f"❌ ERROR: No se pudo abrir el puerto {PUERTO_SERIAL}. ¿Está abierto el Monitor Serial de PlatformIO/IDE o el puerto es incorrecto? ({e})")
    except KeyboardInterrupt:
        print("\nPrueba finalizada por el usuario.")
        if 'ser' in locals() and ser.is_open:
            ser.close()
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

if __name__ == '__main__':
    probar_conexion_serial()