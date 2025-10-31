"""
Instalador Avanzado con Interfaz Mejorada
Incluye splash screen y mejores visuales
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import sys
import os
import threading
from pathlib import Path
import time

class SplashScreen:
    def __init__(self, parent):
        self.parent = parent
        self.splash = tk.Toplevel()
        self.splash.title("")
        self.splash.geometry("400x300")
        self.splash.resizable(False, False)
        self.splash.configure(bg='#2E8B57')
        
        # Centrar la splash screen
        self.splash.transient(parent)
        self.splash.grab_set()
        
        # Configurar splash screen
        self.setup_splash()
        
        # Auto-cerrar después de 3 segundos
        self.splash.after(3000, self.close_splash)
        
    def setup_splash(self):
        # Frame principal
        main_frame = tk.Frame(self.splash, bg='#2E8B57')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título grande
        title_label = tk.Label(main_frame, 
                              text="🦖", 
                              font=("Arial", 48),
                              bg='#2E8B57',
                              fg='white')
        title_label.pack(pady=(20, 10))
        
        # Subtítulo
        subtitle_label = tk.Label(main_frame,
                                 text="JUEGO DINOSAURIO",
                                 font=("Arial", 16, "bold"),
                                 bg='#2E8B57',
                                 fg='white')
        subtitle_label.pack(pady=(0, 10))
        
        # Descripción
        desc_label = tk.Label(main_frame,
                             text="Instalador Automático\nVersión 1.0",
                             font=("Arial", 12),
                             bg='#2E8B57',
                             fg='#E6E6FA',
                             justify=tk.CENTER)
        desc_label.pack(pady=(0, 20))
        
        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill='x', pady=(0, 10))
        self.progress.start()
        
        # Texto de carga
        self.loading_label = tk.Label(main_frame,
                                     text="Iniciando instalador...",
                                     font=("Arial", 10),
                                     bg='#2E8B57',
                                     fg='white')
        self.loading_label.pack()
        
    def close_splash(self):
        self.progress.stop()
        self.splash.destroy()

class InstaladorAvanzado:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🦖 Instalador Juego Dinosaurio v1.0")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # Configurar icono
        try:
            if Path("icon.ico").exists():
                self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Ocultar ventana principal inicialmente
        self.root.withdraw()
        
        # Mostrar splash screen
        splash = SplashScreen(self.root)
        
        # Esperar a que se cierre splash
        self.root.after(3000, self.show_main_window)
        
        # Variables
        self.instalando = False
        self.instalacion_completada = False
        self.progreso_actual = 0
        self.total_pasos = 6  # Total de pasos del proceso
        
    def show_main_window(self):
        self.root.deiconify()
        self.setup_ui()
        
    def setup_ui(self):
        # Configurar tema
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores personalizados
        style.configure('Title.TLabel', font=('Arial', 18, 'bold'), foreground='#2E8B57')
        style.configure('Subtitle.TLabel', font=('Arial', 12), foreground='#555555')
        style.configure('Success.TLabel', font=('Arial', 10, 'bold'), foreground='#4CAF50')
        style.configure('Error.TLabel', font=('Arial', 10, 'bold'), foreground='#f44336')
        
        # Notebook para pestañas
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña principal - Instalación
        self.install_frame = ttk.Frame(notebook)
        notebook.add(self.install_frame, text="🚀 Instalación")
        
        # Pestaña de información
        self.info_frame = ttk.Frame(notebook)
        notebook.add(self.info_frame, text="ℹ️ Información")
        
        self.setup_install_tab()
        self.setup_info_tab()
        
    def setup_install_tab(self):
        # Frame principal con padding
        main_frame = ttk.Frame(self.install_frame, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Encabezado con logo e información
        header_frame = tk.Frame(main_frame, bg='#f8f9fa', relief='groove', bd=2)
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Logo (emoji grande)
        logo_label = tk.Label(header_frame, text="🦖", font=("Arial", 48), bg='#f8f9fa')
        logo_label.pack(side='left', padx=(20, 10), pady=10)
        
        # Información del juego
        info_frame = tk.Frame(header_frame, bg='#f8f9fa')
        info_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        title_label = tk.Label(info_frame, text="JUEGO DINOSAURIO", 
                              font=('Arial', 18, 'bold'), 
                              bg='#f8f9fa', fg='#2E8B57')
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(info_frame, text="Versión mejorada del clásico juego del dinosaurio", 
                                 font=('Arial', 10), 
                                 bg='#f8f9fa', fg='#555555')
        subtitle_label.pack(anchor='w')
        
        features_text = "✅ Controles mejorados  ✅ Múltiples personajes  ✅ Efectos de sonido"
        features_label = tk.Label(info_frame, text=features_text, 
                                 font=('Arial', 9), 
                                 bg='#f8f9fa', fg='#666666')
        features_label.pack(anchor='w', pady=(5, 0))
        
        # Frame de instalación
        install_frame = ttk.LabelFrame(main_frame, text="Instalación Automática", padding="15")
        install_frame.pack(fill='x', pady=(0, 20))
        
        # Descripción de lo que hace
        desc_text = """🔧 Este instalador realizará automáticamente:
        
• Verificación de Python y dependencias
• Creación de entorno virtual aislado
• Instalación de pygame y mysql-connector
• Compilación del juego a ejecutable .exe
• Creación de acceso directo en el escritorio
• Configuración completa lista para usar"""
        
        desc_label = tk.Label(install_frame, text=desc_text, 
                             font=("Consolas", 9), 
                             justify=tk.LEFT,
                             fg='#333333')
        desc_label.pack(anchor='w')
        
        # Botón principal de instalación
        button_frame = tk.Frame(install_frame)
        button_frame.pack(fill='x', pady=(15, 0))
        
        self.btn_instalar = tk.Button(button_frame, 
                                     text="🚀 INSTALAR TODO AUTOMÁTICAMENTE",
                                     font=("Arial", 14, "bold"),
                                     bg='#4CAF50',
                                     fg='white',
                                     activebackground='#45a049',
                                     pady=15,
                                     cursor='hand2',
                                     command=self.iniciar_instalacion)
        self.btn_instalar.pack(fill='x')
        
        # Frame de progreso
        progress_frame = ttk.LabelFrame(main_frame, text="Progreso de Instalación", padding="15")
        progress_frame.pack(fill='both', expand=True)
        
        # Barra de progreso con porcentaje
        self.progress = ttk.Progressbar(progress_frame, mode='determinate', maximum=100)
        self.progress.pack(fill='x', pady=(0, 5))
        
        # Etiqueta de porcentaje
        self.percentage_label = tk.Label(progress_frame, text="0%", 
                                        font=("Arial", 10, "bold"),
                                        fg='#2E8B57')
        self.percentage_label.pack(pady=(0, 5))
        
        # Estado actual
        self.status_label = tk.Label(progress_frame, text="🎯 Listo para instalar", 
                                    font=("Arial", 11, "bold"),
                                    fg='#2E8B57')
        self.status_label.pack(pady=(0, 10))
        
        # Área de log con estilo
        self.log_text = scrolledtext.ScrolledText(progress_frame, 
                                                 height=8, 
                                                 font=("Consolas", 9),
                                                 bg='#f8f9fa',
                                                 fg='#333333',
                                                 relief='groove',
                                                 bd=1)
        self.log_text.pack(fill='both', expand=True, pady=(0, 10))
        
        # Botones de acción
        action_frame = tk.Frame(progress_frame)
        action_frame.pack(fill='x')
        
        self.btn_ejecutar = tk.Button(action_frame, 
                                     text="🎮 Ejecutar Juego",
                                     font=("Arial", 10, "bold"),
                                     bg='#2196F3',
                                     fg='white',
                                     state="disabled",
                                     cursor='hand2',
                                     command=self.ejecutar_juego)
        self.btn_ejecutar.pack(side='left', padx=(0, 10))
        
        self.btn_abrir_carpeta = tk.Button(action_frame, 
                                          text="📁 Abrir Carpeta",
                                          font=("Arial", 10),
                                          bg='#FF9800',
                                          fg='white',
                                          cursor='hand2',
                                          command=self.abrir_carpeta)
        self.btn_abrir_carpeta.pack(side='left', padx=(0, 10))
        
        self.btn_crear_exe = tk.Button(action_frame, 
                                      text="📦 Solo Crear .exe",
                                      font=("Arial", 10),
                                      bg='#9C27B0',
                                      fg='white',
                                      cursor='hand2',
                                      command=self.solo_crear_exe)
        self.btn_crear_exe.pack(side='left', padx=(0, 10))
        
    def setup_info_tab(self):
        info_main = ttk.Frame(self.info_frame, padding="20")
        info_main.pack(fill='both', expand=True)
        
        # Título
        title = tk.Label(info_main, text="ℹ️ Información del Instalador", 
                        font=('Arial', 16, 'bold'), fg='#2E8B57')
        title.pack(pady=(0, 20))
        
        # Información del sistema
        system_frame = ttk.LabelFrame(info_main, text="Información del Sistema", padding="10")
        system_frame.pack(fill='x', pady=(0, 15))
        
        system_info = f"""🖥️ Sistema Operativo: {os.name}
🐍 Python: {sys.version.split()[0]}
📁 Directorio de trabajo: {Path.cwd()}
💾 Espacio requerido: ~500 MB"""
        
        system_label = tk.Label(system_frame, text=system_info, 
                               font=('Consolas', 10), justify='left')
        system_label.pack(anchor='w')
        
        # Requisitos
        req_frame = ttk.LabelFrame(info_main, text="Requisitos", padding="10")
        req_frame.pack(fill='x', pady=(0, 15))
        
        req_info = """✅ Python 3.8 o superior
✅ Conexión a internet (para descargar dependencias)
✅ 500 MB de espacio libre
✅ Windows 10/11 (recomendado)"""
        
        req_label = tk.Label(req_frame, text=req_info, 
                            font=('Consolas', 10), justify='left')
        req_label.pack(anchor='w')
        
        # Qué incluye
        include_frame = ttk.LabelFrame(info_main, text="Qué incluye la instalación", padding="10")
        include_frame.pack(fill='x', pady=(0, 15))
        
        include_info = """🎮 Juego completo del Dinosaurio con mejoras
📦 Ejecutable .exe independiente
🎵 Efectos de sonido y música
🖼️ Gráficos y sprites del juego
🗄️ Sistema de ranking con base de datos
🔧 Todas las dependencias necesarias"""
        
        include_label = tk.Label(include_frame, text=include_info, 
                                font=('Consolas', 10), justify='left')
        include_label.pack(anchor='w')
        
        # Créditos
        credits_frame = ttk.LabelFrame(info_main, text="Desarrollado por", padding="10")
        credits_frame.pack(fill='x')
        
        credits_info = """👥 Equipo de desarrollo:
• Alma Carena
• Facundo Noriega  
• Mateo Lugo
• Santino Trevisano
• Severino Bassus

🔗 GitHub: FacundoTecnica1/Proyecto-ProgramacionPy"""
        
        credits_label = tk.Label(credits_frame, text=credits_info, 
                                font=('Consolas', 10), justify='left')
        credits_label.pack(anchor='w')
        
    def log(self, mensaje, color='black'):
        """Agregar mensaje al log con color"""
        self.log_text.insert(tk.END, f"{mensaje}\n")
        
        # Configurar color si es necesario
        if color != 'black':
            start_line = self.log_text.index(tk.END + "-2l linestart")
            end_line = self.log_text.index(tk.END + "-1l lineend")
            self.log_text.tag_add(color, start_line, end_line)
            self.log_text.tag_config(color, foreground=color)
        
        self.log_text.see(tk.END)
        self.root.update()
        
    def actualizar_progreso(self, paso, mensaje):
        """Actualizar barra de progreso y porcentaje"""
        self.progreso_actual = paso
        porcentaje = int((paso / self.total_pasos) * 100)
        self.progress['value'] = porcentaje
        self.percentage_label.config(text=f"{porcentaje}%")
        self.actualizar_estado(f"📊 {mensaje} ({porcentaje}%)")
        self.root.update()
    
    def actualizar_estado(self, mensaje, color='#2E8B57'):
        """Actualizar etiqueta de estado"""
        self.status_label.config(text=mensaje, fg=color)
        self.root.update()
        
    def ejecutar_comando(self, comando, descripcion):
        """Ejecutar comando y mostrar resultado"""
        self.log(f"🔄 {descripcion}...", 'blue')
        try:
            if isinstance(comando, str):
                resultado = subprocess.run(comando, shell=True, check=True, 
                                         capture_output=True, text=True)
            else:
                resultado = subprocess.run(comando, check=True, 
                                         capture_output=True, text=True)
            
            self.log(f"✅ {descripcion} - COMPLETADO", 'green')
            if resultado.stdout and len(resultado.stdout.strip()) < 200:
                self.log(f"   {resultado.stdout.strip()}")
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"❌ {descripcion} - ERROR", 'red')
            self.log(f"   {e.stderr.strip()}", 'red')
            return False
        except Exception as e:
            self.log(f"❌ {descripcion} - ERROR: {str(e)}", 'red')
            return False
    
    # [El resto de métodos permanecen igual que en la versión anterior]
    def verificar_python(self):
        """Verificar instalación de Python"""
        self.actualizar_progreso(1, "Verificando Python")
        try:
            version = sys.version_info
            version_str = f"{version.major}.{version.minor}.{version.micro}"
            self.log(f"✅ Python {version_str} detectado", 'green')
            
            if version.major < 3 or (version.major == 3 and version.minor < 8):
                self.log(f"⚠️  ADVERTENCIA: Se recomienda Python 3.8+", 'orange')
                return messagebox.askyesno("Versión de Python", 
                                         f"Tu versión es {version_str}. ¿Continuar?")
            return True
        except Exception as e:
            self.log(f"❌ Error verificando Python: {e}", 'red')
            return False
    
    def crear_entorno_virtual(self):
        self.actualizar_progreso(2, "Creando entorno virtual")
        proyecto_dir = Path(__file__).parent.parent
        os.chdir(proyecto_dir)
        
        if Path(".venv").exists():
            self.log("ℹ️  Entorno virtual ya existe")
            return True
            
        return self.ejecutar_comando([sys.executable, "-m", "venv", ".venv"], 
                                   "Crear entorno virtual")
    
    def instalar_dependencias(self):
        self.actualizar_progreso(3, "Instalando dependencias")
        proyecto_dir = Path(__file__).parent.parent
        if os.name == 'nt':
            python_exe = proyecto_dir / ".venv" / "Scripts" / "python.exe"
        else:
            python_exe = proyecto_dir / ".venv" / "bin" / "python"
        
        # Verificar requirements.txt en la carpeta instalador
        requirements_file = Path(__file__).parent / "requirements.txt"
        if not requirements_file.exists():
            with open(requirements_file, 'w') as f:
                f.write("pygame>=2.1.0\nmysql-connector-python>=8.0.0\n")
            self.log("📝 Archivo requirements.txt creado")
        
        # Actualizar pip
        self.ejecutar_comando([str(python_exe), "-m", "pip", "install", "--upgrade", "pip"],
                            "Actualizar pip")
        
        return self.ejecutar_comando([str(python_exe), "-m", "pip", "install", "-r", str(requirements_file)],
                                   "Instalar dependencias del juego")
    
    def instalar_pyinstaller(self):
        self.actualizar_progreso(4, "Instalando PyInstaller")
        proyecto_dir = Path(__file__).parent.parent
        if os.name == 'nt':
            python_exe = proyecto_dir / ".venv" / "Scripts" / "python.exe"
        else:
            python_exe = proyecto_dir / ".venv" / "bin" / "python"
        
        return self.ejecutar_comando([str(python_exe), "-m", "pip", "install", "pyinstaller"],
                                   "Instalar PyInstaller")
    
    def crear_ejecutable(self):
        self.actualizar_progreso(5, "Creando ejecutable")
        proyecto_dir = Path(__file__).parent.parent
        os.chdir(proyecto_dir)
        
        if os.name == 'nt':
            pyinstaller_exe = proyecto_dir / ".venv" / "Scripts" / "pyinstaller.exe"
        else:
            pyinstaller_exe = proyecto_dir / ".venv" / "bin" / "pyinstaller"
        
        comando = [
            str(pyinstaller_exe),
            "--onefile",
            "--windowed",
            "--name=JuegoDinosaurio",
            "--add-data=img;img" if os.name == 'nt' else "--add-data=img:img",
            "--add-data=musica;musica" if os.name == 'nt' else "--add-data=musica:musica",
            "--distpath=dist",
            "--clean",
            "scr/main.py"
        ]
        
        # Agregar icono si existe
        icon_path = Path("instalador/icon.ico")
        if icon_path.exists():
            comando.insert(-1, f"--icon={icon_path}")
            self.log("🎨 Usando icono personalizado")
        
        return self.ejecutar_comando(comando, "Crear ejecutable del juego")
    
    def proceso_instalacion(self):
        try:
            self.instalando = True
            self.btn_instalar.config(state="disabled", text="⏳ Instalando...")
            self.progreso_actual = 0
            self.progress['value'] = 0
            self.percentage_label.config(text="0%")
            
            self.log("🚀 INICIANDO INSTALACIÓN AUTOMÁTICA", 'blue')
            self.log("=" * 60)
            
            if not self.verificar_python():
                raise Exception("Python no está disponible")
            
            if not self.crear_entorno_virtual():
                raise Exception("No se pudo crear el entorno virtual")
            
            if not self.instalar_dependencias():
                raise Exception("No se pudieron instalar las dependencias")
            
            if not self.instalar_pyinstaller():
                raise Exception("No se pudo instalar PyInstaller")
            
            if not self.crear_ejecutable():
                raise Exception("No se pudo crear el ejecutable")
            
            # Finalización
            self.actualizar_progreso(6, "Instalación completada")
            self.log("=" * 60)
            self.log("🎉 ¡INSTALACIÓN COMPLETADA CON ÉXITO!", 'green')
            
            # Verificar que el ejecutable se creó
            proyecto_dir = Path(__file__).parent.parent
            exe_path = proyecto_dir / "dist" / "JuegoDinosaurio.exe"
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024*1024)
                self.log(f"📁 Ejecutable: {exe_path}", 'green')
                self.log(f"📏 Tamaño: {size_mb:.1f} MB", 'green')
            
            self.actualizar_estado("🎉 ¡Instalación completada! (100%)", 'green')
            self.btn_ejecutar.config(state="normal")
            self.instalacion_completada = True
            
            messagebox.showinfo("¡Éxito!", 
                              "🎉 ¡Instalación completada con éxito!\n\n"
                              "• Ejecutable creado en dist/JuegoDinosaurio.exe\n"
                              "• El juego está listo para usar\n"
                              "• Puedes distribuir el .exe independientemente")
            
        except Exception as e:
            self.log(f"❌ ERROR CRÍTICO: {str(e)}", 'red')
            self.actualizar_estado("❌ Error en la instalación", 'red')
            messagebox.showerror("Error", f"Error durante la instalación:\n{str(e)}")
        
        finally:
            self.instalando = False
            self.btn_instalar.config(state="normal", text="🚀 INSTALAR TODO AUTOMÁTICAMENTE")
    
    def iniciar_instalacion(self):
        if self.instalando:
            return
        
        respuesta = messagebox.askyesno("Confirmar Instalación",
                                       "🤖 ¿Listo para la instalación automática?\n\n"
                                       "⏱️ Duración estimada: 3-5 minutos\n"
                                       "💾 Espacio requerido: ~500 MB\n\n"
                                       "El instalador hará todo automáticamente.")
        if respuesta:
            self.log_text.delete(1.0, tk.END)
            threading.Thread(target=self.proceso_instalacion, daemon=True).start()
    
    def solo_crear_exe(self):
        """Solo crear el ejecutable sin instalar dependencias"""
        if self.instalando:
            return
            
        respuesta = messagebox.askyesno("Crear Ejecutable",
                                       "📦 ¿Crear solo el ejecutable?\n\n"
                                       "Esto asume que ya tienes:\n"
                                       "• Python y dependencias instaladas\n"
                                       "• Entorno virtual configurado\n\n"
                                       "¿Continuar?")
        if respuesta:
            def crear_solo_exe():
                try:
                    self.instalando = True
                    self.btn_crear_exe.config(state="disabled")
                    self.progreso_actual = 4
                    self.progress['value'] = int((4 / self.total_pasos) * 100)
                    self.percentage_label.config(text=f"{int((4 / self.total_pasos) * 100)}%")
                    
                    self.log("📦 CREANDO SOLO EJECUTABLE", 'blue')
                    self.log("=" * 40)
                    
                    if not self.instalar_pyinstaller():
                        raise Exception("No se pudo instalar PyInstaller")
                    
                    if not self.crear_ejecutable():
                        raise Exception("No se pudo crear el ejecutable")
                    
                    self.actualizar_progreso(6, "Ejecutable creado")
                    self.log("✅ ¡Ejecutable creado con éxito!", 'green')
                    self.btn_ejecutar.config(state="normal")
                    
                except Exception as e:
                    self.log(f"❌ Error: {str(e)}", 'red')
                finally:
                    self.instalando = False
                    self.btn_crear_exe.config(state="normal")
            
            threading.Thread(target=crear_solo_exe, daemon=True).start()
    
    def ejecutar_juego(self):
        try:
            proyecto_dir = Path(__file__).parent.parent
            exe_path = proyecto_dir / "dist" / "JuegoDinosaurio.exe"
            
            if exe_path.exists():
                subprocess.Popen([str(exe_path)])
                self.log("🎮 Juego ejecutado", 'green')
            else:
                messagebox.showerror("Error", "No se encontró el ejecutable del juego")
        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar el juego:\n{str(e)}")
    
    def abrir_carpeta(self):
        try:
            proyecto_dir = Path(__file__).parent.parent
            if os.name == 'nt':
                os.startfile(str(proyecto_dir))
            else:
                subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", str(proyecto_dir)])
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir carpeta:\n{str(e)}")
    
    def run(self):
        self.root.mainloop()

def main():
    app = InstaladorAvanzado()
    app.run()

if __name__ == "__main__":
    main()