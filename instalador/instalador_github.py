"""
Instalador Automático desde GitHub
Descarga el proyecto completo y ejecuta la instalación
"""

import requests
import zipfile
import os
import subprocess
import sys
import tempfile
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import shutil

class InstaladorGitHub:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🦖 Instalador Automático - Juego Dinosaurio")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Variables
        self.descargando = False
        self.proyecto_dir = None
        self.github_url = "https://github.com/FacundoTecnica1/Proyecto-ProgramacionPy/archive/refs/heads/main.zip"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        title_label = tk.Label(main_frame, 
                              text="🦖 INSTALADOR AUTOMÁTICO DESDE GITHUB",
                              font=("Arial", 16, "bold"),
                              fg="#2E8B57")
        title_label.pack(pady=(0, 20))
        
        # Descripción
        desc_text = """¡Instalación completamente automática!

Este instalador hará todo por ti:
🌐 Descarga el proyecto completo desde GitHub
📦 Extrae todos los archivos automáticamente
🔧 Ejecuta el instalador premium con interfaz gráfica
🎮 Crea el ejecutable del juego listo para usar

Solo presiona el botón y espera..."""
        
        desc_label = tk.Label(main_frame, text=desc_text,
                             font=("Arial", 11),
                             justify=tk.LEFT,
                             bg="#f0f0f0",
                             relief="groove",
                             padx=15, pady=15)
        desc_label.pack(fill='x', pady=(0, 20))
        
        # Información del proyecto
        info_frame = tk.LabelFrame(main_frame, text="Información del Proyecto", 
                                  font=("Arial", 10, "bold"))
        info_frame.pack(fill='x', pady=(0, 20))
        
        info_text = """📁 Repositorio: FacundoTecnica1/Proyecto-ProgramacionPy
🌐 URL: https://github.com/FacundoTecnica1/Proyecto-ProgramacionPy
📊 Tamaño: ~50 MB (aproximado)
⏱️ Tiempo estimado: 5-15 minutos"""
        
        info_label = tk.Label(info_frame, text=info_text,
                             font=("Arial", 9),
                             justify=tk.LEFT,
                             padx=10, pady=10)
        info_label.pack(anchor='w')
        
        # Botón principal
        self.btn_instalar = tk.Button(main_frame,
                                     text="🚀 DESCARGAR E INSTALAR AUTOMÁTICAMENTE",
                                     font=("Arial", 12, "bold"),
                                     bg="#4CAF50",
                                     fg="white",
                                     pady=15,
                                     command=self.iniciar_descarga)
        self.btn_instalar.pack(fill='x', pady=(0, 20))
        
        # Frame de progreso
        progress_frame = tk.LabelFrame(main_frame, text="Progreso", 
                                      font=("Arial", 10, "bold"))
        progress_frame.pack(fill='both', expand=True)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(progress_frame, mode='determinate', maximum=100)
        self.progress.pack(fill='x', padx=10, pady=(10, 5))
        
        # Etiqueta de porcentaje
        self.percentage_label = tk.Label(progress_frame, text="0%",
                                        font=("Arial", 10, "bold"),
                                        fg="#2E8B57")
        self.percentage_label.pack(pady=(0, 5))
        
        # Estado actual
        self.status_label = tk.Label(progress_frame, text="Listo para descargar",
                                    font=("Arial", 10),
                                    fg="#666666")
        self.status_label.pack(pady=(0, 10))
        
        # Área de log
        self.log_text = tk.Text(progress_frame, height=8, 
                               font=("Consolas", 9),
                               bg="#f8f9fa", fg="#333333")
        self.log_text.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Scrollbar para el log
        scrollbar = tk.Scrollbar(self.log_text)
        scrollbar.pack(side='right', fill='y')
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)
        
    def log(self, mensaje):
        """Agregar mensaje al log"""
        self.log_text.insert(tk.END, f"{mensaje}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def actualizar_progreso(self, porcentaje, mensaje):
        """Actualizar progreso y estado"""
        self.progress['value'] = porcentaje
        self.percentage_label.config(text=f"{porcentaje}%")
        self.status_label.config(text=mensaje)
        self.root.update()
        
    def descargar_archivo(self, url, destino):
        """Descargar archivo con progreso"""
        try:
            self.log(f"🌐 Descargando desde: {url}")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(destino, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            porcentaje = int((downloaded / total_size) * 20)  # 20% para descarga
                            self.actualizar_progreso(porcentaje, f"Descargando... {downloaded//1024//1024}MB")
                        
            self.log(f"✅ Descarga completada: {destino}")
            return True
            
        except Exception as e:
            self.log(f"❌ Error descargando: {str(e)}")
            return False
    
    def extraer_zip(self, zip_path, destino):
        """Extraer archivo ZIP"""
        try:
            self.actualizar_progreso(25, "Extrayendo archivos...")
            self.log(f"📦 Extrayendo: {zip_path}")
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(destino)
                
            self.actualizar_progreso(40, "Extracción completada")
            self.log(f"✅ Archivos extraídos en: {destino}")
            return True
            
        except Exception as e:
            self.log(f"❌ Error extrayendo: {str(e)}")
            return False
    
    def encontrar_proyecto(self, directorio):
        """Encontrar la carpeta del proyecto extraída"""
        for item in os.listdir(directorio):
            item_path = os.path.join(directorio, item)
            if os.path.isdir(item_path) and "Proyecto-ProgramacionPy" in item:
                return item_path
        return None
    
    def ejecutar_instalador_premium(self, proyecto_dir):
        """Ejecutar el instalador premium del proyecto"""
        try:
            self.actualizar_progreso(50, "Preparando instalador premium...")
            
            instalador_path = os.path.join(proyecto_dir, "instalador", "instalador_premium.py")
            
            if not os.path.exists(instalador_path):
                raise Exception(f"No se encontró el instalador en: {instalador_path}")
            
            self.log(f"🚀 Ejecutando instalador premium...")
            self.actualizar_progreso(60, "Iniciando instalador gráfico...")
            
            # Ejecutar el instalador premium
            proceso = subprocess.Popen([sys.executable, instalador_path], 
                                     cwd=proyecto_dir,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     text=True)
            
            self.log("🎮 Instalador premium iniciado")
            self.log("📋 Sigue las instrucciones en la nueva ventana")
            
            self.actualizar_progreso(100, "Instalador premium ejecutándose...")
            
            return True
            
        except Exception as e:
            self.log(f"❌ Error ejecutando instalador: {str(e)}")
            return False
    
    def proceso_completo(self):
        """Proceso completo de descarga e instalación"""
        try:
            self.descargando = True
            self.btn_instalar.config(state="disabled", text="⏳ Descargando...")
            
            self.log("🚀 INICIANDO DESCARGA AUTOMÁTICA DESDE GITHUB")
            self.log("=" * 60)
            
            # Crear directorio temporal
            temp_dir = tempfile.mkdtemp(prefix="juego_dinosaurio_")
            self.log(f"📁 Directorio temporal: {temp_dir}")
            
            # Descargar archivo ZIP
            zip_path = os.path.join(temp_dir, "proyecto.zip")
            if not self.descargar_archivo(self.github_url, zip_path):
                raise Exception("Error descargando el proyecto")
            
            # Extraer archivo
            if not self.extraer_zip(zip_path, temp_dir):
                raise Exception("Error extrayendo el proyecto")
            
            # Encontrar la carpeta del proyecto
            self.proyecto_dir = self.encontrar_proyecto(temp_dir)
            if not self.proyecto_dir:
                raise Exception("No se encontró la carpeta del proyecto")
            
            self.log(f"📂 Proyecto encontrado: {self.proyecto_dir}")
            
            # Ejecutar instalador premium
            if not self.ejecutar_instalador_premium(self.proyecto_dir):
                raise Exception("Error ejecutando el instalador premium")
            
            self.log("=" * 60)
            self.log("🎉 ¡PROCESO COMPLETADO CON ÉXITO!")
            self.log("")
            self.log("📋 El instalador premium se ha abierto en una nueva ventana")
            self.log("🎮 Sigue las instrucciones para completar la instalación")
            self.log(f"📁 Proyecto guardado en: {self.proyecto_dir}")
            
            messagebox.showinfo("¡Éxito!",
                              "🎉 ¡Descarga completada!\n\n"
                              "• Proyecto descargado desde GitHub\n"
                              "• Instalador premium iniciado\n"
                              "• Sigue las instrucciones en la nueva ventana\n\n"
                              "¡Ya casi tienes tu juego listo!")
            
        except Exception as e:
            self.log(f"❌ ERROR: {str(e)}")
            self.actualizar_progreso(0, "Error en el proceso")
            messagebox.showerror("Error", f"Error durante la descarga:\n{str(e)}")
            
        finally:
            self.descargando = False
            self.btn_instalar.config(state="normal", text="🚀 DESCARGAR E INSTALAR AUTOMÁTICAMENTE")
    
    def iniciar_descarga(self):
        """Iniciar descarga en hilo separado"""
        if self.descargando:
            return
            
        # Verificar conexión a internet
        try:
            requests.get("https://www.google.com", timeout=5)
        except:
            messagebox.showerror("Sin conexión", 
                               "❌ No hay conexión a internet.\n\n"
                               "Verifica tu conexión y vuelve a intentar.")
            return
        
        respuesta = messagebox.askyesno("Confirmar Descarga",
                                       "🌐 ¿Descargar e instalar desde GitHub?\n\n"
                                       "📊 Tamaño: ~50 MB\n"
                                       "⏱️ Tiempo: 5-15 minutos\n"
                                       "📁 Se creará en directorio temporal\n\n"
                                       "¿Continuar?")
        if respuesta:
            self.log_text.delete(1.0, tk.END)
            threading.Thread(target=self.proceso_completo, daemon=True).start()
    
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

def main():
    # Verificar e instalar dependencias necesarias
    try:
        import requests
    except ImportError:
        print("Instalando requests...")
        subprocess.run([sys.executable, "-m", "pip", "install", "requests"])
        import requests
    
    app = InstaladorGitHub()
    app.run()

if __name__ == "__main__":
    main()