# 🦖 Proyecto: Dinosaurio

## 📖 Descripción
Este es un proyecto escolar que replica el clásico juego del Dinosaurio usando Python y Pygame. El juego incluye controles por teclado y soporte experimental para controlar con Arduino (opcional).

En esta rama se han añadido mecánicas adicionales sobre el clásico:
- Agachado en suelo (flecha abajo): comprime la altura del jugador.
- Flotación en aire (mantener abajo mientras se cae): reduce la gravedad para una caída lenta y notable.
- Dash aéreo (combinación SPACE + DOWN o DOWN + SPACE): congelamiento vertical breve que acelera el mundo (efecto de empuje). Dash sólo en el aire, duración 0.2s.

---

## 👥 Integrantes
- Alma Carena
- Facundo Noriega
- Mateo Lugo
- Santino Trevisano
- Severino Bassus

---

## ⚙️ Requisitos
Para ejecutar el proyecto necesitas:
- Python 3.10+ (recomendado 3.11)
- Pygame (recomendado 2.1+ o la versión disponible en PyPI)

Opcional:
- Arduino y librerías/firmware si quieres usar controles físicos (documentación disponible en los archivos del proyecto si aplica).

---

## 🚀 Instalación Súper Fácil

### � INSTALACIÓN AUTOMÁTICA DESDE GITHUB (Recomendado)

**¿Quieres instalar sin descargar nada manualmente? ¡Usa el instalador automático!**

#### Opción 1: Instalador Independiente (Solo 1 archivo)
1. **Descarga solo este archivo:** [`instalar_juego_dinosaurio.py`](instalar_juego_dinosaurio.py)
2. **Ejecuta:** `python instalar_juego_dinosaurio.py`
3. **¡Presiona el botón y espera!** ☕

#### Opción 2: Desde el repositorio clonado
1. **Clona el repo:** `git clone https://github.com/FacundoTecnica1/Proyecto-ProgramacionPy.git`
2. **Ve a la carpeta:** `cd Proyecto-ProgramacionPy/instalador`
3. **Ejecuta:** `DESCARGAR_DESDE_GITHUB.bat` o `python instalador_github.py`

✨ **El instalador automático:**
- 🌐 Descarga todo el proyecto automáticamente
- 📦 Extrae los archivos
- 🚀 Ejecuta el instalador premium
- 🎮 Crea el ejecutable final
- 🦖 ¡Todo con interfaz gráfica y progreso visual!

---

### 🎯 Instalación Manual Local (Si ya tienes el proyecto)

1. **Ve a la carpeta `instalador/`**
2. **Haz doble clic en `INSTALAR_PREMIUM.bat`**
3. **Presiona el botón "🚀 INSTALAR TODO AUTOMÁTICAMENTE"**
4. **¡Espera 5-10 minutos y listo!** ☕

✨ **El instalador incluye:**
- 🖥️ Interfaz gráfica hermosa con icono del dinosaurio 🦖
- 🤖 Instalación completamente automática
- 📦 Crea ejecutable .exe independiente
- 🎮 Botón para ejecutar el juego al finalizar

### 📋 Instalación Manual (Avanzada)

```bash
git clone https://github.com/FacundoTecnica1/Proyecto-ProgramacionPy.git
cd Proyecto-ProgramacionPy
python -m venv .venv
.\.venv\Scripts\activate
pip install -r instalador/requirements.txt
python scr\main.py
```

📖 **Ver [COMO_INSTALAR.txt](COMO_INSTALAR.txt) para más detalles.**

Si tu estructura cambia, ajusta la ruta al archivo principal (`scr\main.py`).

---

## 🕹️ Controles
- SPACE: saltar (si estás en suelo)
- DOWN (flecha abajo): agacharse en suelo; en aire, al mantenerla durante la caída activa la flotación
- Dash aéreo: mantener DOWN y presionar SPACE, o mantener SPACE y presionar DOWN. Dash sólo funciona en aire, dura ~0.2s y tiene un cooldown.

Consejos de prueba:
- Para sentir la flotación: salta y mientras caes mantén la flecha abajo; la caída será más lenta y notoria.
- Para hacer dash: salta, mientras estás en el aire mantén DOWN y presiona SPACE (o al revés). El dash sólo se activará si estás en el aire.

---

## 📂 Estructura del proyecto (resumen)
```
Proyecto-ProgramacionPy/
│
├── scr/                # Código fuente del juego
│   ├── main.py         # Algoritmo principal del juego
│   ├── game_objects.py # Clases de jugador, obstáculos, aves y fondo
│   └── utils.py        # Utilidades
│
├── img/                # Imágenes y sprites
├── musica/             # Archivos de audio
├── tests/              # Scripts de prueba
├── README.md
└── LICENSE
```

---

## 📑 Presentaciones / Documentos (acceso directo)
- Carpeta de Campo (Google Docs): https://docs.google.com/document/d/1PWEvjFt2JRpvwiG7trO7vT8PoXgSzEGUtTOgXIrnGBc/edit?usp=sharing
- Informe Dinosaurio (Google Docs): https://docs.google.com/document/d/1efqNAkmHdIXBj6DLJUk_hXVtkQ_QOHop5NcSbBFXr3A/edit?usp=sharing
- Presentación (Canva): https://www.canva.com/design/DAGzwWcfe3o/Yw7oA71p6piL9RDDVTT9zw/edit?utm_content=DAGzwWcfe3o&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

---

## 📄 Licencia
Este proyecto se distribuye bajo la **MIT License**. Consulta el archivo [LICENSE](./LICENSE) para más información.
