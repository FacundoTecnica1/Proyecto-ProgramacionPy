<?php
$host = "localhost";
$user = "root";
$pass = "";
$dbname = "dino"; // ⚠️ Debe existir en phpMyAdmin

try {
    $conn = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $user, $pass);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("❌ Error de conexión: " . $e->getMessage());
}
?>
