<?php
require_once 'conexion.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Método no permitido']);
    exit;
}

// Verificar si hay sesión activa
if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(['error' => 'No hay sesión activa']);
    exit;
}

try {
    // Desactivar cuenta del usuario
    $stmt = $pdo->prepare("UPDATE usuarios_pagina SET active = 0 WHERE Id_UsuarioPagina = ?");
    $stmt->execute([$_SESSION['user_id']]);
    
    if ($stmt->rowCount() > 0) {
        // Guardar información antes de cerrar sesión
        $username = $_SESSION['username'];
        
        // Cerrar sesión
        session_destroy();
        
        echo json_encode([
            'success' => true,
            'message' => 'Cuenta desactivada exitosamente. Tu cuenta ha sido desactivada temporalmente.',
            'username' => $username
        ]);
    } else {
        http_response_code(404);
        echo json_encode(['error' => 'Usuario no encontrado']);
    }
    
} catch(PDOException $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Error al desactivar cuenta: ' . $e->getMessage()]);
}
?>