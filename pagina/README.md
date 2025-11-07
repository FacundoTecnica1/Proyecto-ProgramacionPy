# 🌐 Configuración de la Página Web del Dino Game

## 📋 Requisitos Previos

1. **XAMPP** instalado y funcionando
2. **MySQL/MariaDB** activo
3. **PHP** habilitado en XAMPP
4. Base de datos `dino` existente

## 🛠️ Configuración de la Base de Datos

### Paso 1: Crear/Actualizar las Tablas

1. Abre **phpMyAdmin** en tu navegador: `http://localhost/phpmyadmin`
2. Selecciona la base de datos `dino`
3. Ve a la pestaña "SQL" 
4. Ejecuta el contenido del archivo `update_database.sql`:

```sql
-- Agregar nuevas columnas a la tabla usuario
ALTER TABLE usuario 
ADD COLUMN email VARCHAR(255) UNIQUE AFTER Nombre,
ADD COLUMN password VARCHAR(255) AFTER email,
ADD COLUMN active TINYINT(1) DEFAULT 1 AFTER password,
ADD COLUMN fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP AFTER active;

-- Crear tabla para sugerencias
CREATE TABLE IF NOT EXISTS sugerencias (
    Id_Sugerencia INT AUTO_INCREMENT PRIMARY KEY,
    Id_Usuario INT NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    categoria ENUM('gameplay', 'graphics', 'audio', 'controls', 'features', 'bugs') NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Id_Usuario) REFERENCES usuario(Id_Usuario) ON DELETE CASCADE
);

-- Insertar algunos datos de ejemplo para las sugerencias (opcional)
INSERT INTO sugerencias (Id_Usuario, titulo, categoria, descripcion) VALUES
(1, 'Mejorar efectos de sonido', 'audio', 'Sería genial tener más variedad en los efectos de sonido del juego'),
(2, 'Agregar más personajes', 'features', 'Me gustaría ver más opciones de personajes además del gato y el perro'),
(3, 'Arreglar lag ocasional', 'bugs', 'A veces el juego se pone lento cuando hay muchos obstáculos');

-- Actualizar usuarios existentes con datos de ejemplo (password: "123456")
UPDATE usuario SET 
    email = CONCAT(LOWER(Nombre), '@example.com'),
    password = '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi'
WHERE password IS NULL;
```

### Paso 2: Verificar la Configuración

1. Asegúrate de que XAMPP esté ejecutándose
2. Verifica que Apache y MySQL estén activos
3. Comprueba que la carpeta del proyecto esté en `htdocs`

## 🚀 Cómo Usar la Página Web

### Acceso
Abre tu navegador y ve a: `http://localhost/Proyecto-ProgramacionPy/pagina/`

### Funcionalidades

#### 🔐 Sistema de Autenticación
- **Registro de usuarios**: Crea una cuenta nueva
- **Inicio de sesión**: Accede con usuario/email y contraseña
- **Gestión de cuenta**: 
  - Desactivar cuenta (temporal)
  - Eliminar cuenta (permanente)

#### 💡 Sistema de Sugerencias
- Solo usuarios autenticados pueden enviar sugerencias
- Categorías disponibles: jugabilidad, gráficos, audio, controles, características, bugs
- Las sugerencias se guardan en la base de datos

#### 🖼️ Galería Dinámica
- El carrusel se conecta a la base de datos
- Carga automáticamente imágenes del directorio `img/`
- Fallback a imágenes predeterminadas si hay problemas

#### 📱 Responsive Design
- Totalmente adaptado para móviles y tablets
- Menú hamburguesa en dispositivos pequeños
- Gestos touch para el carrusel

## 🔧 Configuración de la API

### Archivo `api.php`
El archivo maneja todas las operaciones de backend:

- `?action=register` - Registro de usuarios
- `?action=login` - Inicio de sesión
- `?action=logout` - Cerrar sesión  
- `?action=delete_account` - Eliminar cuenta
- `?action=deactivate_account` - Desactivar cuenta
- `?action=add_suggestion` - Agregar sugerencia
- `?action=get_suggestions` - Obtener sugerencias
- `?action=get_gallery_images` - Obtener imágenes de galería
- `?action=check_session` - Verificar sesión activa

### Configuración de Base de Datos
En `api.php`, líneas 3-6:
```php
$host = 'localhost';
$username = 'root';
$password = '';
$database = 'dino';
```

## 🐛 Solución de Problemas

### Error: "No se puede conectar a la base de datos"
1. Verifica que MySQL esté ejecutándose en XAMPP
2. Comprueba que la base de datos `dino` exista
3. Asegúrate de que las credenciales en `api.php` sean correctas

### Error: "Tabla no existe"
1. Ejecuta el script `update_database.sql` en phpMyAdmin
2. Verifica que todas las tablas se hayan creado correctamente

### El carrusel no carga imágenes
1. Verifica que el directorio `img/` contenga imágenes
2. Comprueba los permisos de archivo
3. Revisa la consola del navegador para errores

### Problemas de autenticación
1. Verifica que PHP sessions estén habilitadas
2. Comprueba que no haya errores en la consola del navegador
3. Asegúrate de que la API responda correctamente

## 📂 Estructura de Archivos

```
pagina/
├── index.html          # Página principal
├── styles.css          # Estilos CSS
├── script.js           # JavaScript principal
├── api.php             # Backend API
├── update_database.sql # Script de actualización BD
├── manual-usuario.html # Manual de usuario (legacy)
└── README.md           # Este archivo
```

## 🔗 Enlaces Importantes

- **Manual de Usuario**: https://docs.google.com/document/d/1ztkTsi6y9YvGDC7K-BrUiye13_bU1RyW0znbrmTO70o/edit?usp=sharing
- **Repositorio GitHub**: https://github.com/FacundoTecnica1/Proyecto-ProgramacionPy
- **Descarga del Juego**: https://raw.githubusercontent.com/FacundoTecnica1/Proyecto-ProgramacionPy/main/DinoSetup.exe

## 🎮 Cambios en las Mecánicas del Juego

Se han eliminado las siguientes mecánicas de la documentación:
- ❌ **Dash aéreo** (ESPACIO + ↓)
- ❌ **Flotación** (mantener ↓ mientras se cae)

Mecánicas actuales:
- ✅ **Saltar** (ESPACIO o ↑)
- ✅ **Agacharse** (↓)
- ✅ **Navegación en menús** (← →)
- ✅ **Pausar** (ESC)

## 📞 Soporte

Si encuentras problemas:
1. Revisa esta documentación
2. Verifica la configuración de XAMPP
3. Comprueba los logs de error de PHP
4. Usa las herramientas de desarrollador del navegador para debugger

---

**Nota**: Esta página web está diseñada para funcionar en un entorno local con XAMPP. Para producción, necesitarías ajustar la configuración de seguridad y base de datos.