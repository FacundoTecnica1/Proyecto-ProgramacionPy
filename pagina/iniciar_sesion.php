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
if (empty($input['username']) || empty($input['password'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Usuario y contraseña son requeridos']);
    exit;
}

$username = sanitizeInput($input['username']);
$password = $input['password'];

try {
    // Buscar usuario por nombre o email
    $stmt = $pdo->prepare("SELECT Id_UsuarioPagina, NomUsuario, email, password, active FROM usuarios_pagina WHERE NomUsuario = ? OR email = ?");
    $stmt->execute([$username, $username]);
    $user = $stmt->fetch(PDO::FETCH_ASSOC);
    
    if (!$user) {
        http_response_code(401);
        echo json_encode(['error' => 'Usuario no encontrado']);
        exit;
    }
    
    // Verificar contraseña
    if (!password_verify($password, $user['password'])) {
        http_response_code(401);
        echo json_encode(['error' => 'Contraseña incorrecta']);
        exit;
    }
    
    // Verificar si la cuenta está activa
    if (!$user['active']) {
        http_response_code(403);
        echo json_encode(['error' => 'Cuenta desactivada. Contacta al administrador.']);
        exit;
    }
    
    // Guardar en sesión
    $_SESSION['user_id'] = $user['Id_UsuarioPagina'];
    $_SESSION['username'] = $user['NomUsuario'];
    $_SESSION['email'] = $user['email'];
    
    echo json_encode([
        'success' => true,
        'message' => 'Inicio de sesión exitoso',
        'username' => $user['NomUsuario']
    ]);
    
} catch(PDOException $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Error al iniciar sesión: ' . $e->getMessage()]);
}
?>