<?php
require_once 'conexion.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Método no permitido']);
    exit;
}

// Obtener datos JSON
$input = json_decode(file_get_contents('php://input'), true);

// Validar datos requeridos
if (empty($input['username']) || empty($input['email']) || empty($input['password'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Todos los campos son requeridos']);
    exit;
}

$username = sanitizeInput($input['username']);
$email = sanitizeInput($input['email']);
$password = $input['password'];

// Validar email
if (!validateEmail($email)) {
    http_response_code(400);
    echo json_encode(['error' => 'Email no válido']);
    exit;
}

// Validar contraseña
if (strlen($password) < 6) {
    http_response_code(400);
    echo json_encode(['error' => 'La contraseña debe tener al menos 6 caracteres']);
    exit;
}

try {
    // Verificar si el usuario o email ya existe
    $stmt = $pdo->prepare("SELECT Id_UsuarioPagina FROM usuarios_pagina WHERE NomUsuario = ? OR email = ?");
    $stmt->execute([$username, $email]);
    
    if ($stmt->rowCount() > 0) {
        http_response_code(409);
        echo json_encode(['error' => 'El usuario o email ya existe']);
        exit;
    }
    
    // Encriptar contraseña
    $passwordHash = password_hash($password, PASSWORD_DEFAULT);
    
    // Insertar nuevo usuario
    $stmt = $pdo->prepare("INSERT INTO usuarios_pagina (NomUsuario, email, password, active, fecha_registro) VALUES (?, ?, ?, 1, NOW())");
    $stmt->execute([$username, $email, $passwordHash]);
    
    $userId = $pdo->lastInsertId();
    
    // Guardar en sesión
    $_SESSION['user_id'] = $userId;
    $_SESSION['username'] = $username;
    $_SESSION['email'] = $email;
    
    echo json_encode([
        'success' => true,
        'message' => 'Usuario registrado exitosamente',
        'username' => $username
    ]);
    
} catch(PDOException $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Error al registrar usuario: ' . $e->getMessage()]);
}
?>