<?php
// Configuración de la base de datos
$host = 'localhost';
$username = 'root';
$password = '';
$database = 'dino';

// Habilitar CORS para peticiones AJAX
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json; charset=utf-8');

try {
    $pdo = new PDO("mysql:host=$host;dbname=$database;charset=utf8mb4", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Error de conexión a la base de datos: ' . $e->getMessage()]);
    exit;
}

// Obtener método HTTP y acción
$method = $_SERVER['REQUEST_METHOD'];
$input = json_decode(file_get_contents('php://input'), true);
$action = $_GET['action'] ?? '';

// Función para validar datos
function validateInput($data, $required_fields) {
    foreach ($required_fields as $field) {
        if (empty($data[$field])) {
            return false;
        }
    }
    return true;
}

// Función para sanitizar datos
function sanitizeInput($data) {
    return htmlspecialchars(strip_tags(trim($data)));
}

// Routing basado en la acción
switch ($action) {
    case 'register':
        handleRegister();
        break;
    case 'login':
        handleLogin();
        break;
    case 'logout':
        handleLogout();
        break;
    case 'delete_account':
        handleDeleteAccount();
        break;
    case 'deactivate_account':
        handleDeactivateAccount();
        break;
    case 'add_suggestion':
        handleAddSuggestion();
        break;
    case 'get_suggestions':
        handleGetSuggestions();
        break;
    case 'get_gallery_images':
        handleGetGalleryImages();
        break;
    case 'check_session':
        handleCheckSession();
        break;
    default:
        http_response_code(400);
        echo json_encode(['error' => 'Acción no válida']);
        break;
}

function handleRegister() {
    global $pdo, $input;
    
    if (!validateInput($input, ['username', 'email', 'password'])) {
        http_response_code(400);
        echo json_encode(['error' => 'Todos los campos son requeridos']);
        return;
    }
    
    $username = sanitizeInput($input['username']);
    $email = sanitizeInput($input['email']);
    $password = password_hash($input['password'], PASSWORD_DEFAULT);
    
    try {
        // Verificar si el usuario ya existe
        $stmt = $pdo->prepare("SELECT Id_Usuario FROM usuario WHERE Nombre = ? OR email = ?");
        $stmt->execute([$username, $email]);
        
        if ($stmt->rowCount() > 0) {
            http_response_code(409);
            echo json_encode(['error' => 'El usuario o email ya existe']);
            return;
        }
        
        // Insertar nuevo usuario
        $stmt = $pdo->prepare("INSERT INTO usuario (Nombre, email, password, active) VALUES (?, ?, ?, 1)");
        $stmt->execute([$username, $email, $password]);
        
        $userId = $pdo->lastInsertId();
        
        // Iniciar sesión
        session_start();
        $_SESSION['user_id'] = $userId;
        $_SESSION['username'] = $username;
        
        echo json_encode([
            'success' => true,
            'message' => 'Usuario registrado exitosamente',
            'user' => ['id' => $userId, 'username' => $username]
        ]);
        
    } catch(PDOException $e) {
        http_response_code(500);
        echo json_encode(['error' => 'Error al registrar usuario: ' . $e->getMessage()]);
    }
}

function handleLogin() {
    global $pdo, $input;
    
    if (!validateInput($input, ['username', 'password'])) {
        http_response_code(400);
        echo json_encode(['error' => 'Usuario y contraseña son requeridos']);
        return;
    }
    
    $username = sanitizeInput($input['username']);
    $password = $input['password'];
    
    try {
        $stmt = $pdo->prepare("SELECT Id_Usuario, Nombre, password, active FROM usuario WHERE Nombre = ? OR email = ?");
        $stmt->execute([$username, $username]);
        $user = $stmt->fetch(PDO::FETCH_ASSOC);
        
        if ($user && password_verify($password, $user['password'])) {
            if (!$user['active']) {
                http_response_code(403);
                echo json_encode(['error' => 'Cuenta desactivada']);
                return;
            }
            
            session_start();
            $_SESSION['user_id'] = $user['Id_Usuario'];
            $_SESSION['username'] = $user['Nombre'];
            
            echo json_encode([
                'success' => true,
                'message' => 'Inicio de sesión exitoso',
                'user' => ['id' => $user['Id_Usuario'], 'username' => $user['Nombre']]
            ]);
        } else {
            http_response_code(401);
            echo json_encode(['error' => 'Credenciales incorrectas']);
        }
        
    } catch(PDOException $e) {
        http_response_code(500);
        echo json_encode(['error' => 'Error al iniciar sesión: ' . $e->getMessage()]);
    }
}

function handleLogout() {
    session_start();
    session_destroy();
    echo json_encode(['success' => true, 'message' => 'Sesión cerrada exitosamente']);
}

function handleDeleteAccount() {
    global $pdo;
    session_start();
    
    if (!isset($_SESSION['user_id'])) {
        http_response_code(401);
        echo json_encode(['error' => 'No hay sesión activa']);
        return;
    }
    
    try {
        $pdo->beginTransaction();
        
        // Eliminar sugerencias del usuario
        $stmt = $pdo->prepare("DELETE FROM sugerencias WHERE Id_Usuario = ?");
        $stmt->execute([$_SESSION['user_id']]);
        
        // Eliminar ranking del usuario
        $stmt = $pdo->prepare("DELETE FROM ranking WHERE Id_Usuario = ?");
        $stmt->execute([$_SESSION['user_id']]);
        
        // Eliminar usuario
        $stmt = $pdo->prepare("DELETE FROM usuario WHERE Id_Usuario = ?");
        $stmt->execute([$_SESSION['user_id']]);
        
        $pdo->commit();
        session_destroy();
        
        echo json_encode(['success' => true, 'message' => 'Cuenta eliminada exitosamente']);
        
    } catch(PDOException $e) {
        $pdo->rollBack();
        http_response_code(500);
        echo json_encode(['error' => 'Error al eliminar cuenta: ' . $e->getMessage()]);
    }
}

function handleDeactivateAccount() {
    global $pdo;
    session_start();
    
    if (!isset($_SESSION['user_id'])) {
        http_response_code(401);
        echo json_encode(['error' => 'No hay sesión activa']);
        return;
    }
    
    try {
        $stmt = $pdo->prepare("UPDATE usuario SET active = 0 WHERE Id_Usuario = ?");
        $stmt->execute([$_SESSION['user_id']]);
        
        session_destroy();
        
        echo json_encode(['success' => true, 'message' => 'Cuenta desactivada exitosamente']);
        
    } catch(PDOException $e) {
        http_response_code(500);
        echo json_encode(['error' => 'Error al desactivar cuenta: ' . $e->getMessage()]);
    }
}

function handleAddSuggestion() {
    global $pdo, $input;
    session_start();
    
    if (!isset($_SESSION['user_id'])) {
        http_response_code(401);
        echo json_encode(['error' => 'Debes iniciar sesión para enviar sugerencias']);
        return;
    }
    
    if (!validateInput($input, ['title', 'category', 'description'])) {
        http_response_code(400);
        echo json_encode(['error' => 'Todos los campos son requeridos']);
        return;
    }
    
    $title = sanitizeInput($input['title']);
    $category = sanitizeInput($input['category']);
    $description = sanitizeInput($input['description']);
    
    try {
        $stmt = $pdo->prepare("INSERT INTO sugerencias (Id_Usuario, titulo, categoria, descripcion, fecha_creacion) VALUES (?, ?, ?, ?, NOW())");
        $stmt->execute([$_SESSION['user_id'], $title, $category, $description]);
        
        echo json_encode(['success' => true, 'message' => 'Sugerencia enviada exitosamente']);
        
    } catch(PDOException $e) {
        http_response_code(500);
        echo json_encode(['error' => 'Error al enviar sugerencia: ' . $e->getMessage()]);
    }
}

function handleGetSuggestions() {
    global $pdo;
    
    try {
        $stmt = $pdo->prepare("
            SELECT s.titulo, s.categoria, s.descripcion, s.fecha_creacion, u.Nombre 
            FROM sugerencias s 
            JOIN usuario u ON s.Id_Usuario = u.Id_Usuario 
            ORDER BY s.fecha_creacion DESC 
            LIMIT 10
        ");
        $stmt->execute();
        $suggestions = $stmt->fetchAll(PDO::FETCH_ASSOC);
        
        echo json_encode(['success' => true, 'suggestions' => $suggestions]);
        
    } catch(PDOException $e) {
        http_response_code(500);
        echo json_encode(['error' => 'Error al obtener sugerencias: ' . $e->getMessage()]);
    }
}

function handleGetGalleryImages() {
    // Listar imágenes disponibles del juego
    $imageDir = '../img/';
    $allowedExtensions = ['png', 'jpg', 'jpeg', 'gif'];
    $images = [];
    
    if (is_dir($imageDir)) {
        $files = scandir($imageDir);
        foreach ($files as $file) {
            $extension = strtolower(pathinfo($file, PATHINFO_EXTENSION));
            if (in_array($extension, $allowedExtensions)) {
                $images[] = [
                    'src' => '../img/' . $file,
                    'caption' => ucfirst(str_replace(['_', '.png', '.jpg', '.jpeg', '.gif'], [' ', '', '', '', ''], $file))
                ];
            }
        }
    }
    
    echo json_encode(['success' => true, 'images' => $images]);
}

function handleCheckSession() {
    session_start();
    
    if (isset($_SESSION['user_id'])) {
        echo json_encode([
            'success' => true,
            'logged_in' => true,
            'user' => [
                'id' => $_SESSION['user_id'],
                'username' => $_SESSION['username']
            ]
        ]);
    } else {
        echo json_encode([
            'success' => true,
            'logged_in' => false
        ]);
    }
}
?>