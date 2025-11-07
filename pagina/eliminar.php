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
    $user_id = $_SESSION['user_id'];
    
    // Iniciar transacción
    $pdo->beginTransaction();
    
    // Eliminar sugerencias del usuario
    $stmt = $pdo->prepare("DELETE FROM sugerencias WHERE Id_UsuarioPagina = ?");
    $stmt->execute([$user_id]);
    
    // Eliminar registros de ranking del usuario (si los hubiera)
    // $stmt = $pdo->prepare("DELETE FROM ranking WHERE Id_Usuario = ?");
    // $stmt->execute([$user_id]);
    
    // Eliminar usuario
    $stmt = $pdo->prepare("DELETE FROM usuarios_pagina WHERE Id_UsuarioPagina = ?");
    $stmt->execute([$user_id]);
    
    if ($stmt->rowCount() > 0) {
        // Confirmar transacción
        $pdo->commit();
        
        // Guardar información antes de cerrar sesión
        $username = $_SESSION['username'];
        
        // Cerrar sesión
        session_destroy();
        
        echo json_encode([
            'success' => true,
            'message' => 'Cuenta eliminada exitosamente. Tu cuenta y todos tus datos han sido eliminados permanentemente.',
            'username' => $username
        ]);
    } else {
        // Revertir transacción
        $pdo->rollBack();
        http_response_code(404);
        echo json_encode(['error' => 'Usuario no encontrado']);
    }
    
} catch(PDOException $e) {
    // Revertir transacción en caso de error
    $pdo->rollBack();
    http_response_code(500);
    echo json_encode(['error' => 'Error al eliminar cuenta: ' . $e->getMessage()]);
}
?>