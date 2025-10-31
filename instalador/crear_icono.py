"""
Crear icono para el juego del dinosaurio
Genera un archivo .ico usando PIL/Pillow
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    def crear_icono_dinosaurio():
        # Crear imagen de 256x256 (tamaño estándar para iconos)
        size = 256
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))  # Fondo transparente
        draw = ImageDraw.Draw(img)
        
        # Colores
        verde_dino = (34, 139, 34)  # Verde del dinosaurio
        amarillo = (255, 215, 0)   # Detalles
        negro = (0, 0, 0)          # Contornos
        blanco = (255, 255, 255)   # Ojos
        
        # Dibujar el cuerpo del dinosaurio (forma simplificada)
        # Cuerpo principal
        draw.ellipse([50, 120, 200, 220], fill=verde_dino, outline=negro, width=3)
        
        # Cabeza
        draw.ellipse([160, 80, 240, 160], fill=verde_dino, outline=negro, width=3)
        
        # Cuello
        draw.polygon([(170, 120), (200, 100), (200, 140), (170, 160)], 
                    fill=verde_dino, outline=negro)
        
        # Cola
        draw.polygon([(50, 140), (20, 120), (10, 160), (30, 180), (50, 170)], 
                    fill=verde_dino, outline=negro)
        
        # Patas
        # Pata trasera
        draw.rectangle([80, 200, 100, 240], fill=verde_dino, outline=negro, width=2)
        draw.ellipse([75, 235, 105, 250], fill=verde_dino, outline=negro, width=2)
        
        # Pata delantera
        draw.rectangle([140, 200, 160, 240], fill=verde_dino, outline=negro, width=2)
        draw.ellipse([135, 235, 165, 250], fill=verde_dino, outline=negro, width=2)
        
        # Ojos
        draw.ellipse([180, 100, 200, 120], fill=blanco, outline=negro, width=2)
        draw.ellipse([200, 100, 220, 120], fill=blanco, outline=negro, width=2)
        
        # Pupilas
        draw.ellipse([185, 105, 195, 115], fill=negro)
        draw.ellipse([205, 105, 215, 115], fill=negro)
        
        # Boca
        draw.arc([170, 130, 210, 150], start=0, end=180, fill=negro, width=3)
        
        # Detalles decorativos (rayas en el lomo)
        for i in range(3):
            y = 130 + i * 15
            draw.line([60 + i*5, y, 100 + i*5, y], fill=amarillo, width=3)
        
        # Guardar como .ico con múltiples tamaños
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        icons = []
        
        for icon_size in icon_sizes:
            resized_img = img.resize(icon_size, Image.Resampling.LANCZOS)
            icons.append(resized_img)
        
        # Guardar el icono
        icon_path = "icon.ico"
        icons[0].save(icon_path, format='ICO', sizes=icon_sizes)
        print(f"✅ Icono creado: {icon_path}")
        
        # También crear PNG para uso general
        img.save("icon.png", format='PNG')
        print("✅ Imagen PNG creada: icon.png")
        
        return True
        
    if __name__ == "__main__":
        crear_icono_dinosaurio()
        
except ImportError:
    print("⚠️  PIL/Pillow no está instalado.")
    print("Ejecutando: pip install Pillow")
    
    import subprocess
    try:
        subprocess.run(["pip", "install", "Pillow"], check=True)
        print("✅ Pillow instalado. Ejecuta el script nuevamente.")
    except:
        print("❌ No se pudo instalar Pillow automáticamente.")
        print("Instálalo manualmente: pip install Pillow")