-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 07-11-2025 a las 13:13:43
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `dino`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ranking`
--

CREATE TABLE `ranking` (
  `Id_Ranking` int(11) NOT NULL,
  `Puntaje` int(11) NOT NULL,
  `Id_Usuario` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ranking`
--

INSERT INTO `ranking` (`Id_Ranking`, `Puntaje`, `Id_Usuario`) VALUES
(1, 1500, 1),
(2, 1200, 2),
(3, 1800, 3),
(4, 900, 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `Id_Usuario` int(11) NOT NULL,
  `Nombre` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`Id_Usuario`, `Nombre`) VALUES
(1, 'Alma'),
(2, 'Santino'),
(3, 'Nicolás'),
(4, 'Malena');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios_pagina`
--

CREATE TABLE `usuarios_pagina` (
  `Id_UsuarioPagina` int(11) NOT NULL,
  `NomUsuario` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `active` tinyint(1) DEFAULT 1,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sugerencias`
--

CREATE TABLE `sugerencias` (
  `Id_Sugerencia` int(11) NOT NULL,
  `Id_UsuarioPagina` int(11) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `categoria` enum('gameplay','graphics','audio','controls','features','bugs') NOT NULL,
  `descripcion` text NOT NULL,
  `valoracion` int(1) DEFAULT 0 CHECK (valoracion >= 1 AND valoracion <= 5),
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `sugerencias`
--

INSERT INTO `sugerencias` (`Id_Sugerencia`, `Id_UsuarioPagina`, `titulo`, `categoria`, `descripcion`, `valoracion`, `fecha_creacion`) VALUES
(1, 1, 'Mejorar efectos de sonido', 'audio', 'Sería genial tener más variedad en los efectos de sonido del juego', 4, '2024-11-07 12:30:00'),
(2, 2, 'Agregar más personajes', 'features', 'Me gustaría ver más opciones de personajes además del gato y el perro', 5, '2024-11-07 13:00:00'),
(3, 3, 'Arreglar lag ocasional', 'bugs', 'A veces el juego se pone lento cuando hay muchos obstáculos', 3, '2024-11-07 13:30:00');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `ranking`
--
ALTER TABLE `ranking`
  ADD PRIMARY KEY (`Id_Ranking`),
  ADD KEY `Id_Usuario` (`Id_Usuario`);

--
-- Indices de la tabla `sugerencias`
--
ALTER TABLE `sugerencias`
  ADD PRIMARY KEY (`Id_Sugerencia`),
  ADD KEY `Id_UsuarioPagina` (`Id_UsuarioPagina`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`Id_Usuario`),
  ADD UNIQUE KEY `Nombre` (`Nombre`);

--
-- Indices de la tabla `usuarios_pagina`
--
ALTER TABLE `usuarios_pagina`
  ADD PRIMARY KEY (`Id_UsuarioPagina`),
  ADD UNIQUE KEY `NomUsuario` (`NomUsuario`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `sugerencias`
--
ALTER TABLE `sugerencias`
  MODIFY `Id_Sugerencia` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `ranking`
--
ALTER TABLE `ranking`
  MODIFY `Id_Ranking` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `Id_Usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `usuarios_pagina`
--
ALTER TABLE `usuarios_pagina`
  MODIFY `Id_UsuarioPagina` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `sugerencias`
--
ALTER TABLE `sugerencias`
  ADD CONSTRAINT `sugerencias_ibfk_1` FOREIGN KEY (`Id_UsuarioPagina`) REFERENCES `usuarios_pagina` (`Id_UsuarioPagina`) ON DELETE CASCADE;

--
-- Filtros para la tabla `ranking`
--
ALTER TABLE `ranking`
  ADD CONSTRAINT `ranking_ibfk_1` FOREIGN KEY (`Id_Usuario`) REFERENCES `usuario` (`Id_Usuario`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
