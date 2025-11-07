<?php
require_once 'conexion.php';

// Verificar si hay sesión activa para enviar sugerencias
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'enviar') {
    if (!isset($_SESSION['user_id'])) {
        http_response_code(401);
        echo json_encode(['error' => 'Debes estar registrado para enviar sugerencias']);
        exit;
    }
    
    try {
        $user_id = $_SESSION['user_id'];
        $sugerencia = trim($_POST['sugerencia']);
        $valoracion = (int)$_POST['valoracion'];
        
        if (empty($sugerencia)) {
            http_response_code(400);
            echo json_encode(['error' => 'La sugerencia no puede estar vacía']);
            exit;
        }
        
        if ($valoracion < 1 || $valoracion > 5) {
            http_response_code(400);
            echo json_encode(['error' => 'La valoración debe estar entre 1 y 5 estrellas']);
            exit;
        }
        
        // Insertar sugerencia
        $stmt = $pdo->prepare("INSERT INTO sugerencias (Id_UsuarioPagina, titulo, categoria, descripcion, valoracion, fecha_creacion) VALUES (?, ?, ?, ?, ?, NOW())");
        $stmt->execute([$user_id, 'Sugerencia de usuario', 'features', $sugerencia, $valoracion]);
        
        echo json_encode([
            'success' => true,
            'message' => 'Sugerencia enviada exitosamente. ¡Gracias por tu feedback!'
        ]);
        
    } catch(PDOException $e) {
        http_response_code(500);
        echo json_encode(['error' => 'Error al enviar sugerencia: ' . $e->getMessage()]);
    }
    exit;
}

// Obtener sugerencias (GET)
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    try {
        $page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
        $limit = 10;
        $offset = ($page - 1) * $limit;
        
        // Obtener total de sugerencias
        $stmt = $pdo->query("SELECT COUNT(*) FROM sugerencias");
        $total = $stmt->fetchColumn();
        
        // Obtener sugerencias con información del usuario
        $stmt = $pdo->prepare("
            SELECT s.descripcion as sugerencia, s.valoracion, s.fecha_creacion as fecha, u.NomUsuario 
            FROM sugerencias s 
            JOIN usuarios_pagina u ON s.Id_UsuarioPagina = u.Id_UsuarioPagina 
            ORDER BY s.fecha_creacion DESC 
            LIMIT ? OFFSET ?
        ");
        $stmt->execute([$limit, $offset]);
        $sugerencias = $stmt->fetchAll(PDO::FETCH_ASSOC);
        
        echo json_encode([
            'success' => true,
            'sugerencias' => $sugerencias,
            'total' => $total,
            'page' => $page,
            'pages' => ceil($total / $limit)
        ]);
        
    } catch(PDOException $e) {
        http_response_code(500);
        echo json_encode(['error' => 'Error al obtener sugerencias: ' . $e->getMessage()]);
    }
    exit;
}

// Eliminar sugerencia (solo el propietario)
if ($_SERVER['REQUEST_METHOD'] === 'DELETE') {
    if (!isset($_SESSION['user_id'])) {
        http_response_code(401);
        echo json_encode(['error' => 'No hay sesión activa']);
        exit;
    }
    
    parse_str(file_get_contents('php://input'), $data);
    $sugerencia_id = (int)$data['id'];
    
    try {
        // Verificar que la sugerencia pertenece al usuario
        $stmt = $pdo->prepare("DELETE FROM sugerencias WHERE id = ? AND Id_UsuarioPagina = ?");
        $stmt->execute([$sugerencia_id, $_SESSION['user_id']]);
        
        if ($stmt->rowCount() > 0) {
            echo json_encode([
                'success' => true,
                'message' => 'Sugerencia eliminada exitosamente'
            ]);
        } else {
            http_response_code(404);
            echo json_encode(['error' => 'Sugerencia no encontrada o no tienes permisos para eliminarla']);
        }
        
    } catch(PDOException $e) {
        http_response_code(500);
        echo json_encode(['error' => 'Error al eliminar sugerencia: ' . $e->getMessage()]);
    }
    exit;
}

http_response_code(405);
echo json_encode(['error' => 'Método no permitido']);
?>