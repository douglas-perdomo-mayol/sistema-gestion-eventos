-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: eventos_db
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `cedula` varchar(20) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `direccion` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cedula` (`cedula`),
  UNIQUE KEY `correo` (`correo`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `cliente_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES (1,22,'Douglas','Perdomo','402-11999884-7','douglasjpm1217@gmail.com','809-232-4323','Arenoso'),(2,22,'Luis','Garcia','031-0000000-0','luis@gmail.com','809-000-0000','Punal'),(3,22,'Maria','Gomez','021-9999999-9','maria1221@hotmail.com','829-090-7766','Los Gomez'),(4,22,'Maria','Sanchez','321-0000000-2','maria@gmail.com','890-000-9999','Los cabrales'),(5,28,'Mario','Garcias','402-0099887-0','mario23@gmail.com','809-909-3243','Licey al medio');
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evento`
--

DROP TABLE IF EXISTS `evento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `evento` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `descripcion` text,
  `fecha_inicio` date NOT NULL,
  `fecha_final` date NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_final` time NOT NULL,
  `ubicacion` varchar(255) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `capacidad` int NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `estado` varchar(50) NOT NULL,
  `estado_pago` enum('pendiente','pagado') DEFAULT 'pendiente',
  PRIMARY KEY (`id`),
  KEY `id_cliente` (`id_cliente`),
  CONSTRAINT `evento_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evento`
--

LOCK TABLES `evento` WRITE;
/*!40000 ALTER TABLE `evento` DISABLE KEYS */;
INSERT INTO `evento` VALUES (5,1,'Fiesta','Lo mejor','2024-07-05','2024-07-05','10:00:00','11:00:00','Arenoso','Otro',400,1000.00,'Activo','pagado'),(6,1,'Cumplianos','Para la mejor','2024-07-05','2024-07-05','14:00:00','17:00:00','Canabacoa','Otro',400,5000.00,'Finalizado','pendiente'),(7,1,'Fiesta Familiar','El rencuentro','2024-07-06','2024-07-06','08:00:00','10:00:00','Arenoso, Punal','Otro',100,1000.00,'Pendiente','pagado'),(9,1,'Festibal del humor','Un lugar para olvidar lo malo','2024-07-12','2024-07-12','09:00:00','10:00:00','Laguna prieta','Humor',1000,1000.00,'Activo','pendiente'),(10,1,'Fiesta','Lo mejor','2024-07-12','2024-07-12','01:00:00','03:00:00','Arenoso','Otro',500,1000.00,'Pendiente','pendiente'),(11,2,'Festival del humor','Lugar para reir','2024-07-12','2024-07-12','14:00:00','17:00:00','Matanza','Conferencia',400,5000.00,'Activo','pagado'),(12,2,'Boda','Un dia de paz y amor','2024-07-13','2024-07-13','14:00:00','18:00:00','Puntacana','Seminario',500,5000.00,'Pendiente','pendiente'),(13,5,'Cumple 15','Lo mejor','2024-07-14','2024-07-14','14:00:00','17:00:00','Arenoso','Otro',500,5000.00,'Pendiente','pendiente');
/*!40000 ALTER TABLE `evento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transacciones`
--

DROP TABLE IF EXISTS `transacciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transacciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int NOT NULL,
  `id_evento` int NOT NULL,
  `fecha` date NOT NULL,
  `monto_pagado` decimal(10,2) NOT NULL,
  `metodo_pago` varchar(50) NOT NULL,
  `estado_transaccion` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_cliente` (`id_cliente`),
  KEY `id_evento` (`id_evento`),
  CONSTRAINT `transacciones_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id`),
  CONSTRAINT `transacciones_ibfk_2` FOREIGN KEY (`id_evento`) REFERENCES `evento` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transacciones`
--

LOCK TABLES `transacciones` WRITE;
/*!40000 ALTER TABLE `transacciones` DISABLE KEYS */;
INSERT INTO `transacciones` VALUES (11,1,5,'2024-07-05',1000.00,'Tarjeta de Débito','Completado'),(12,1,6,'2024-07-05',4000.00,'Tarjeta de Crédito','Pendiente'),(13,1,6,'2024-07-05',1000.00,'Tarjeta de Crédito','Completado'),(14,1,5,'2024-07-05',100.00,'Tarjeta de Crédito','Pendiente'),(15,1,5,'2024-07-05',900.00,'Tarjeta de Débito','Completado'),(16,1,5,'2024-07-05',1000.00,'Tarjeta de Crédito','Completado'),(17,1,6,'2024-07-05',100.00,'Tarjeta de Débito','Completado'),(18,1,6,'2024-07-06',4900.00,'Tarjeta de Débito','Completado'),(19,1,6,'2024-07-05',1000.00,'Tarjeta de Débito','Pendiente'),(20,1,6,'2024-07-05',4000.00,'Tarjeta de Débito','Completado'),(21,1,7,'2024-07-06',1000.00,'Transferencia Bancaria','Completado'),(22,2,11,'2024-07-13',5000.00,'PayPal','Completado'),(23,2,11,'2024-07-13',5000.00,'Transferencia Bancaria','Completado');
/*!40000 ALTER TABLE `transacciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_usuario` varchar(255) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `foto_perfil` varchar(255) DEFAULT NULL,
  `fecha_registro` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre_usuario` (`nombre_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (2,'Maria','4321',NULL,NULL),(4,'Luis','123456',NULL,NULL),(22,'Douglas','12345678','C:/Users/DOUGLAS/Desktop/hola.jpg',NULL),(25,'Pedro','1234',NULL,NULL),(26,'Carlos','12345678',NULL,NULL),(27,'Lisa','87654321',NULL,NULL),(28,'Saul','kLp2397Ms','C:/Users/DOUGLAS/Desktop/fotos ingienería II/Captura de pantalla 2024-06-18 155050.png',NULL),(29,'David','12345678',NULL,NULL);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-16 13:38:02
