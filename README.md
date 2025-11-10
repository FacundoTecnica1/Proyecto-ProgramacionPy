## 🦖 Proyecto: Dinosaurio

## 📖 Descripción
Este es un proyecto escolar que replica el clásico juego del Dinosaurio usando Python y Pygame. El juego incluye controles por teclado y soporte experimental para controlar con Arduino (opcional).

En esta rama se han añadido mecánicas adicionales sobre el clásico:
- Agachado en suelo (flecha abajo): comprime la altura del jugador.
- Flotación en aire (mantener abajo mientras se cae): reduce la gravedad para una caída lenta y notable.

---

## 👥 Integrantes
- Alma Carena
- Facundo Noriega
- Mateo Lugo
- Santino Trevisano
- Severino Bassus

---

## 🚀 Instalación y Ejecución (Windows)

Hay dos formas de jugar: **descargando el ejecutable** o **ejecutando desde el código fuente**.

### Opción 1: Descargar el Instalador (Recomendado para jugar rápido) 🚀
Descarga el instalador del juego para Windows directamente. Haz clic derecho y selecciona "Guardar enlace como..." si la descarga no inicia automáticamente.

➡️ **[Descargar DinoSetup.exe](https://raw.githubusercontent.com/FacundoTecnica1/Proyecto-ProgramacionPy/main/DinoSetup.exe)** ⬅️
> **Nota:** Si el archivo .exe está en una carpeta diferente, debes cambiar la ruta en el enlace (por ejemplo, si está en la raíz, usa: `.../Proyecto-ProgramacionPy/main/DinoSetup.exe`).

---

### Opción 2: Ejecutar desde el Código Fuente (Requiere Python)

#### ⚙️ Requisitos
Para ejecutar el proyecto necesitas:
- Python 3.10+ (recomendado 3.11)
- Pygame (recomendado 2.1+ o la versión disponible en PyPI)

Opcional:
- Arduino y librerías/firmware si quieres usar controles físicos (documentación disponible en los archivos del proyecto si aplica).

#### Pasos para la Ejecución
1. Clonar el repositorio

```powershell
git clone [https://github.com/FacundoTecnica1/Proyecto-ProgramacionPy.git](https://github.com/FacundoTecnica1/Proyecto-ProgramacionPy.git)
cd Proyecto-ProgramacionPy

### Ejecutar con Python

Instala dependencias y ejecuta desde el código (útil para desarrollo):

```powershell
python -m pip install -r requirements.txt  # si existe, o instalar pygame y demás manualmente
python -m pip install pyserial
python -m scr.main
```

Si usas el Arduino, conecta el dispositivo y verifica el puerto serie antes de iniciar:

```python
import serial.tools.list_ports
print(list(serial.tools.list_ports.comports()))
```

## Construir el .exe con PyInstaller

Se provee un archivo de especificación `DinoRunExtreme.spec` en la raíz. Recomendado usar `python -m PyInstaller` para evitar problemas de PATH.

Pasos rápidos:

1. Instala PyInstaller en el mismo intérprete que usas para el proyecto:

```powershell
python -m pip install pyinstaller
```

2. Asegúrate de que `pyserial` está instalado (es necesario para detectarlo en tiempo de ejecución):

```powershell
python -m pip install pyserial
```

3. Edita `DinoRunExtreme.spec` si necesitas añadir módulos ocultos (hiddenimports). Ejemplo mínimo para incluir pyserial:

```python
hiddenimports=[
	'pymysql',
	'serial',
	'serial.tools.list_ports',
]
```

4. Compila con PyInstaller usando el .spec (desde la carpeta del proyecto):

```powershell
python -m PyInstaller DinoRunExtreme.spec
```

5. El ejecutable generado estará en `dist/DinoRunExtreme/`. El instalador `DinoSetup.iss` está preparado para copiar `DinoRunExtreme.exe` (renombrándolo a `Dino.exe`) y la carpeta `_internal` con todas las DLL y recursos.

### Problemas comunes con Arduino / pyserial en el .exe

- El .exe puede fallar al abrir el puerto serie si `pyserial` no fue incluido. Asegúrate de añadir `serial` y `serial.tools.list_ports` en `hiddenimports` del `.spec`.
- Ejecuta el .exe desde PowerShell para ver mensajes de error (muchas veces el fallo es una excepción de import o permiso):

```powershell
cd dist\DinoRunExtreme
.\DinoRunExtreme.exe
```

- Comprueba que el Arduino esté conectado y que los drivers estén instalados. En Windows revisa el Administrador de dispositivos -> Puertos (COM & LPT).
- Si el programa se comporta distinto cuando se empaqueta: prueba ejecutar el script con el mismo intérprete y las mismas variables de entorno que usa PyInstaller.
- Si usas un instalador, asegúrate de copiar la carpeta `_internal` completa (donde PyInstaller coloca bibliotecas, recursos y módulos nativos). El `DinoSetup.iss` incluido ya apunta a `dist\DinoRunExtreme\_internal`.

## Crear el instalador (Inno Setup)

El script `DinoSetup.iss` está en la raíz y ya configurado para copiar:

- `dist\DinoRunExtreme\DinoRunExtreme.exe` como `Dino.exe`
- todo `dist\DinoRunExtreme\_internal\*` a `{app}\_internal`
- `INSTRUCCIONES.txt` y (opcional) `rank_debug.log`

Compila el instalador con Inno Setup Compiler y prueba la instalación en una máquina con el Arduino conectado para verificar que detecta el puerto.

## Solución rápida de Git (push falla por timeout / conexión)

Si `git push` falla con errores como `RPC failed; curl 55` o `HTTP 408`, prueba aumentar el buffer y reintentar:

```powershell
git config --global http.postBuffer 524288000
git push origin main
```

También revisa tu conexión a Internet, desactiva VPN/proxy temporalmente y prueba desde otra red si es posible.

## Depuración rápida

- Ejecuta el ejecutable desde PowerShell para ver trazas:

```powershell
cd dist\DinoRunExtreme
.\DinoRunExtreme.exe
```

- Para ver puertos serie disponibles (útil si Arduino no se detecta):

```powershell
python - <<'PY'
import serial.tools.list_ports
print(list(serial.tools.list_ports.comports()))
PY
```

## Notas y buenas prácticas

- Mantén `pyserial` en las dependencias del entorno donde compilas.
- Evita empujar archivos binarios grandes al repositorio (usa release assets o Git LFS si necesitas subir ejecutables grandes).
- Antes de distribuir, prueba la instalación en una máquina limpia (sin Python) para validar que el instalador copia `_internal` correctamente.

---

Si quieres, puedo:

- Generar un `requirements.txt` mínimo
- Ejecutar PyInstaller localmente (si me indicas que lo haga aquí)
- Probar y ajustar `DinoRunExtreme.spec` para asegurar que pyserial y demás módulos nativos se incluyan

Marca la tarea en progreso cuando quieras que haga alguno de esos pasos.
