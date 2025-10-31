"""
🦖 INSTALADOR INDEPENDIENTE - JUEGO DINOSAURIO
Descarga automáticamente desde GitHub y ejecuta la instalación completa

INSTRUCCIONES:
1. Guarda este archivo como "instalar_juego_dinosaurio.py"
2. Ejecuta: python instalar_juego_dinosaurio.py
3. ¡Sigue las instrucciones en pantalla!

NO NECESITAS DESCARGAR NADA MÁS - Este archivo hace todo automáticamente
"""

import os
import sys
import subprocess
import tempfile
import zipfile
from pathlib import Path

# Verificar e instalar dependencias automáticamente
def instalar_dependencias():
    """Instalar dependencias necesarias"""
    dependencias = ['requests', 'tkinter']
    
    for dep in dependencias:
        try:
            if dep == 'tkinter':
                import tkinter
            else:
                __import__(dep)
        except ImportError:
            print(f"📦 Instalando {dep}...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                         capture_output=True)

# Instalar dependencias al inicio
instalar_dependencias()

# Ahora importar todo lo necesario
import requests
import tkinter as tk
from tkinter import ttk, messagebox
import threading

class InstaladorIndependiente:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🦖 Instalador Juego Dinosaurio - Desde GitHub")
        self.root.geometry("650x550")
        self.root.resizable(False, False)
        
        # Configuración
        self.github_url = "https://github.com/FacundoTecnica1/Proyecto-ProgramacionPy/archive/refs/heads/main.zip"
        self.descargando = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal con padding
        main_frame = tk.Frame(self.root, padx=25, pady=25, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True)
        
        # Header con emoji y título
        header_frame = tk.Frame(main_frame, bg='#f8f9fa')
        header_frame.pack(fill='x', pady=(0, 25))
        
        emoji_label = tk.Label(header_frame, text="🦖", font=("Arial", 48), bg='#f8f9fa')
        emoji_label.pack()
        
        title_label = tk.Label(header_frame, 
                              text="INSTALADOR AUTOMÁTICO DESDE GITHUB",
                              font=("Arial", 16, "bold"),
                              fg="#2E8B57", bg='#f8f9fa')
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame,
                                 text="Descarga e instala el Juego Dinosaurio automáticamente",
                                 font=("Arial", 11),
                                 fg="#666666", bg='#f8f9fa')
        subtitle_label.pack(pady=(5, 0))
        
        # Información del proceso
        info_frame = tk.LabelFrame(main_frame, text="🔄 Qué hace este instalador", 
                                  font=("Arial", 11, "bold"),
                                  padx=15, pady=15)
        info_frame.pack(fill='x', pady=(0, 20))
        
        info_text = """✅ Descarga el proyecto completo desde GitHub (FacundoTecnica1/Proyecto-ProgramacionPy)
✅ Extrae todos los archivos automáticamente
✅ Verifica que Python esté instalado correctamente
✅ Ejecuta el instalador premium con interfaz gráfica
✅ Instala todas las dependencias (pygame, mysql-connector)
✅ Crea el ejecutable del juego con icono personalizado
✅ Deja todo listo para jugar inmediatamente

🎮 ¡Solo necesitas hacer 1 clic y esperar!"""
        
        info_label = tk.Label(info_frame, text=info_text,
                             font=("Arial", 10),
                             justify=tk.LEFT,
                             fg="#333333")
        info_label.pack(anchor='w')
        
        # Botón principal súper llamativo
        self.btn_principal = tk.Button(main_frame,
                                      text="🚀 ¡DESCARGAR E INSTALAR AHORA!",
                                      font=("Arial", 14, "bold"),
                                      bg="#4CAF50",
                                      fg="white",
                                      activebackground="#45a049",
                                      activeforeground="white",
                                      pady=20,
                                      cursor="hand2",
                                      relief="raised",
                                      bd=3,
                                      command=self.iniciar_proceso)
        self.btn_principal.pack(fill='x', pady=(0, 20))
        
        # Frame de progreso
        progress_frame = tk.LabelFrame(main_frame, text="📊 Progreso de Instalación",
                                      font=("Arial", 11, "bold"),
                                      padx=15, pady=15)
        progress_frame.pack(fill='both', expand=True)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(progress_frame, mode='determinate', maximum=100)
        self.progress.pack(fill='x', pady=(0, 10))
        
        # Porcentaje y estado
        status_frame = tk.Frame(progress_frame)
        status_frame.pack(fill='x', pady=(0, 10))
        
        self.percentage_label = tk.Label(status_frame, text="0%",
                                        font=("Arial", 12, "bold"),
                                        fg="#2E8B57")
        self.percentage_label.pack(side='left')
        
        self.status_label = tk.Label(status_frame, text="Listo para comenzar",
                                    font=("Arial", 10),
                                    fg="#666666")
        self.status_label.pack(side='right')
        
        # Log de actividad
        self.log_text = tk.Text(progress_frame, height=8,
                               font=("Consolas", 9),
                               bg="#ffffff",
                               fg="#333333",
                               relief="sunken",
                               bd=2)
        self.log_text.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(self.log_text)
        scrollbar.pack(side='right', fill='y')
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)
        
        # Footer con información
        footer_frame = tk.Frame(main_frame, bg='#f8f9fa')
        footer_frame.pack(fill='x', pady=(15, 0))
        
        footer_text = "💡 Tip: Este proceso puede tardar 5-15 minutos dependiendo de tu conexión a internet"
        footer_label = tk.Label(footer_frame, text=footer_text,
                               font=("Arial", 9),
                               fg="#888888", bg='#f8f9fa')
        footer_label.pack()
        
    def log(self, mensaje):
        """Agregar mensaje al log"""
        self.log_text.insert(tk.END, f"{mensaje}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def actualizar_progreso(self, porcentaje, estado):
        """Actualizar progreso"""
        self.progress['value'] = porcentaje
        self.percentage_label.config(text=f"{porcentaje}%")
        self.status_label.config(text=estado)
        self.root.update()
        
    def verificar_requisitos(self):
        """Verificar requisitos del sistema"""
        self.actualizar_progreso(5, "Verificando requisitos...")
        self.log("🔍 Verificando requisitos del sistema...")
        
        # Verificar Python
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            self.log(f"⚠️  Python {version.major}.{version.minor} detectado")
            self.log("🔧 Se recomienda Python 3.8 o superior")
        else:
            self.log(f"✅ Python {version.major}.{version.minor} - Correcto")
        
        # Verificar conexión
        try:
            requests.get("https://www.google.com", timeout=5)
            self.log("✅ Conexión a internet - Correcta")
            return True
        except:
            self.log("❌ Sin conexión a internet")
            messagebox.showerror("Error", "❌ No hay conexión a internet.\nVerifica tu conexión.")
            return False
    
    def descargar_proyecto(self):
        """Descargar proyecto desde GitHub"""
        self.actualizar_progreso(10, "Descargando desde GitHub...")
        self.log(f"🌐 Descargando: {self.github_url}")
        
        try:
            # Crear directorio temporal
            self.temp_dir = tempfile.mkdtemp(prefix="juego_dinosaurio_")
            zip_path = os.path.join(self.temp_dir, "proyecto.zip")
            
            # Descargar con progreso
            response = requests.get(self.github_url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(zip_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            progreso = 10 + int((downloaded / total_size) * 30)  # 10-40%
                            mb_downloaded = downloaded / 1024 / 1024
                            mb_total = total_size / 1024 / 1024
                            self.actualizar_progreso(progreso, 
                                                   f"Descargando {mb_downloaded:.1f}/{mb_total:.1f} MB")
            
            self.log(f"✅ Descarga completada: {downloaded/1024/1024:.1f} MB")
            self.zip_path = zip_path
            return True
            
        except Exception as e:
            self.log(f"❌ Error descargando: {str(e)}")
            return False
    
    def extraer_proyecto(self):
        """Extraer proyecto descargado"""
        self.actualizar_progreso(45, "Extrayendo archivos...")
        self.log("📦 Extrayendo archivos del proyecto...")
        
        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)
            
            # Encontrar carpeta del proyecto
            for item in os.listdir(self.temp_dir):
                item_path = os.path.join(self.temp_dir, item)
                if os.path.isdir(item_path) and "Proyecto-ProgramacionPy" in item:
                    self.proyecto_dir = item_path
                    break
            
            if not hasattr(self, 'proyecto_dir'):
                raise Exception("No se encontró la carpeta del proyecto")
            
            self.actualizar_progreso(60, "Extracción completada")
            self.log(f"✅ Proyecto extraído en: {self.proyecto_dir}")
            return True
            
        except Exception as e:
            self.log(f"❌ Error extrayendo: {str(e)}")
            return False
    
    def ejecutar_instalador_premium(self):
        """Ejecutar instalador premium"""
        self.actualizar_progreso(70, "Iniciando instalador premium...")
        self.log("🚀 Preparando instalador premium...")
        
        try:
            instalador_path = os.path.join(self.proyecto_dir, "instalador", "instalador_premium.py")
            
            if not os.path.exists(instalador_path):
                raise Exception("No se encontró el instalador premium")
            
            self.log("🎮 Ejecutando instalador premium...")
            self.log("📋 Se abrirá una nueva ventana - sigue las instrucciones")
            
            # Ejecutar instalador premium
            subprocess.Popen([sys.executable, instalador_path], cwd=self.proyecto_dir)
            
            self.actualizar_progreso(100, "¡Instalador premium ejecutándose!")
            self.log("=" * 50)
            self.log("🎉 ¡PROCESO COMPLETADO CON ÉXITO!")
            self.log("📋 El instalador premium se abrió en una nueva ventana")
            self.log("🎮 Sigue las instrucciones para completar la instalación")
            self.log(f"📁 Proyecto guardado en: {self.proyecto_dir}")
            
            messagebox.showinfo("¡Éxito!",
                              "🎉 ¡Descarga completada!\n\n"
                              "✅ Proyecto descargado desde GitHub\n"
                              "✅ Instalador premium iniciado\n\n"
                              "🎮 Sigue las instrucciones en la nueva ventana\n"
                              "para completar la instalación del juego!")
            
            return True
            
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
            return False
    
    def proceso_completo(self):
        """Proceso completo de instalación"""
        try:
            self.descargando = True
            self.btn_principal.config(state="disabled", text="⏳ Procesando...")
            
            self.log("🦖 INSTALADOR AUTOMÁTICO - JUEGO DINOSAURIO")
            self.log("=" * 50)
            
            # Verificar requisitos
            if not self.verificar_requisitos():
                return
            
            # Descargar proyecto
            if not self.descargar_proyecto():
                raise Exception("Error en la descarga")
            
            # Extraer proyecto
            if not self.extraer_proyecto():
                raise Exception("Error en la extracción")
            
            # Ejecutar instalador premium
            if not self.ejecutar_instalador_premium():
                raise Exception("Error ejecutando instalador")
            
        except Exception as e:
            self.log(f"❌ ERROR CRÍTICO: {str(e)}")
            self.actualizar_progreso(0, "Error en el proceso")
            messagebox.showerror("Error", f"Error durante la instalación:\n{str(e)}")
            
        finally:
            self.descargando = False
            self.btn_principal.config(state="normal", text="🚀 ¡DESCARGAR E INSTALAR AHORA!")
    
    def iniciar_proceso(self):
        """Iniciar proceso en hilo separado"""
        if self.descargando:
            return
        
        respuesta = messagebox.askyesno("Confirmar Instalación",
                                       "🌐 ¿Descargar e instalar desde GitHub?\n\n"
                                       "📊 Tamaño: ~50 MB\n"
                                       "⏱️ Tiempo: 5-15 minutos\n"
                                       "🎮 Incluye instalación completa del juego\n\n"
                                       "¿Continuar?")
        if respuesta:
            self.log_text.delete(1.0, tk.END)
            threading.Thread(target=self.proceso_completo, daemon=True).start()
    
    def run(self):
        """Ejecutar aplicación"""
        self.root.mainloop()

def main():
    """Función principal"""
    print("🦖 Iniciando Instalador Automático - Juego Dinosaurio")
    print("📱 Abriendo interfaz gráfica...")
    
    app = InstaladorIndependiente()
    app.run()

if __name__ == "__main__":
    main()