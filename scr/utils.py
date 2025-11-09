import pygame

def mostrar_texto(texto, x, y, color, pantalla, tam=30, centrado=False, sombra=True, fuente_personalizada=None):
    """
    Función mejorada para mostrar texto con sombra y mejor tipografía
    """
    try:
        # Usar fuente personalizada si se proporciona, sino usar la por defecto
        if fuente_personalizada:
            fuente = fuente_personalizada
        else:
            fuente = pygame.font.Font(None, tam)
        
        # Dibujar sombra primero (si está habilitada)
        if sombra:
            superficie_sombra = fuente.render(str(texto), True, (0, 0, 0))  # Sombra negra
            rect_sombra = superficie_sombra.get_rect()
            if centrado:
                rect_sombra.center = (x + 2, y + 2)  # Desplazar sombra
            else:
                rect_sombra.topleft = (x + 2, y + 2)
            pantalla.blit(superficie_sombra, rect_sombra)
        
        # Dibujar texto principal
        superficie = fuente.render(str(texto), True, color)
        rect = superficie.get_rect()
        if centrado:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        pantalla.blit(superficie, rect)
        
    except Exception as e:
        # Fallback simple si hay error
        try:
            fuente_simple = pygame.font.Font(None, tam)
            superficie = fuente_simple.render(str(texto), True, color)
            rect = superficie.get_rect()
            if centrado:
                rect.center = (x, y)
            else:
                rect.topleft = (x, y)
            pantalla.blit(superficie, rect)
        except:
            pass  # Si todo falla, no mostrar nada

def mostrar_texto_con_fondo(texto, x, y, color_texto, color_fondo, pantalla, tam=30, centrado=False, padding=8):
    """
    Muestra texto con un fondo semitransparente
    """
    try:
        fuente = pygame.font.Font(None, tam)
        superficie = fuente.render(str(texto), True, color_texto)
        rect = superficie.get_rect()
        
        if centrado:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        
        # Crear fondo con padding
        fondo_rect = rect.inflate(padding * 2, padding)
        fondo_surface = pygame.Surface(fondo_rect.size, pygame.SRCALPHA)
        
        # Asegurar que color_fondo tenga solo RGB
        if len(color_fondo) >= 3:
            color_rgb = color_fondo[:3]  # Tomar solo RGB
        else:
            color_rgb = (50, 50, 50)  # Fallback
            
        fondo_surface.fill((*color_rgb, 180))  # Fondo semitransparente
        
        # Dibujar fondo redondeado
        pygame.draw.rect(fondo_surface, (*color_rgb, 180), fondo_surface.get_rect(), border_radius=8)
        pantalla.blit(fondo_surface, fondo_rect.topleft)
        
        # Dibujar texto encima
        pantalla.blit(superficie, rect)
        
    except Exception as e:
        # Fallback: usar mostrar_texto simple si hay error
        mostrar_texto(texto, x, y, color_texto, pantalla, tam, centrado, sombra=True)

def crear_fuente_titulo():
    """Crea una fuente para títulos"""
    try:
        return pygame.font.Font(None, 48)
    except:
        return pygame.font.Font(None, 48)

def crear_fuente_hud():
    """Crea una fuente para el HUD del juego"""
    try:
        return pygame.font.Font(None, 36)
    except:
        return pygame.font.Font(None, 36)

def crear_fuente_gameover():
    """Crea una fuente para game over"""
    try:
        return pygame.font.Font(None, 42)
    except:
        return pygame.font.Font(None, 42)
