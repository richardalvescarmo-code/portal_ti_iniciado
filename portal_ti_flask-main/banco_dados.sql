CREATE DATABASE  IF NOT EXISTS `portal_ti` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `portal_ti`;
-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: portal_ti
-- ------------------------------------------------------
-- Server version	8.0.46

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
-- Table structure for table `auditoria`
--

DROP TABLE IF EXISTS `auditoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auditoria` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `acao` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `modulo` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `registro` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `data` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auditoria`
--

LOCK TABLES `auditoria` WRITE;
/*!40000 ALTER TABLE `auditoria` DISABLE KEYS */;
INSERT INTO `auditoria` VALUES (1,'Administrador','Editou','Softwares','Google Chrome','2026-08-03 17:16:32'),(2,'Administrador','Criou','Softwares','Java','2026-08-04 11:24:25');
/*!40000 ALTER TABLE `auditoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cofre_discos`
--

DROP TABLE IF EXISTS `cofre_discos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cofre_discos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `identificacao_maquina` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `serial_disco` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fornecedor` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `data_envio` date DEFAULT NULL,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Armazenado',
  `observacao` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `criado_em` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `atualizado_em` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cofre_discos`
--

LOCK TABLES `cofre_discos` WRITE;
/*!40000 ALTER TABLE `cofre_discos` DISABLE KEYS */;
/*!40000 ALTER TABLE `cofre_discos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ferramentas`
--

DROP TABLE IF EXISTS `ferramentas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ferramentas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `categoria` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `descricao` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `url_acesso` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `icone` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'bi-tools',
  `ativo` tinyint(1) NOT NULL DEFAULT '1',
  `criado_em` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `atualizado_em` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ferramentas`
--

LOCK TABLES `ferramentas` WRITE;
/*!40000 ALTER TABLE `ferramentas` DISABLE KEYS */;
INSERT INTO `ferramentas` VALUES (1,'Grafana','Monitoramento','Acessar monitoramentos das redes','https://grafana.hugtak.com/','bi-graph-up-arrow',1,'2026-08-03 14:32:49','2026-08-03 14:32:49');
/*!40000 ALTER TABLE `ferramentas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `filtros_privacidade`
--

DROP TABLE IF EXISTS `filtros_privacidade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `filtros_privacidade` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `quantidade` int NOT NULL DEFAULT '0',
  `observacao` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `atualizado_em` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filtros_privacidade`
--

LOCK TABLES `filtros_privacidade` WRITE;
/*!40000 ALTER TABLE `filtros_privacidade` DISABLE KEYS */;
INSERT INTO `filtros_privacidade` VALUES (1,'Notebook',0,NULL,'2026-08-03 11:43:10'),(2,'Desktop',4,NULL,'2026-08-03 16:06:09');
/*!40000 ALTER TABLE `filtros_privacidade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `procedimentos`
--

DROP TABLE IF EXISTS `procedimentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `procedimentos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `categoria` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `descricao` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `conteudo` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `arquivo_nome` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `arquivo_original` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ativo` tinyint(1) NOT NULL DEFAULT '1',
  `criado_em` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `atualizado_em` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `procedimentos`
--

LOCK TABLES `procedimentos` WRITE;
/*!40000 ALTER TABLE `procedimentos` DISABLE KEYS */;
INSERT INTO `procedimentos` VALUES (1,'Configuração VPN','VPN','Esse procedimento mostra como instalar e configurar o Forticlient VPN.','Procedimento em anexo.','4881583262484926954f9c4600ce6da4.pdf','instalacaovpn.pdf',1,'2026-08-03 13:42:55','2026-08-03 13:42:55');
/*!40000 ALTER TABLE `procedimentos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `softwares`
--

DROP TABLE IF EXISTS `softwares`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `softwares` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descricao` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `categoria` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `icone` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'bi-box-seam',
  `url_download` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ativo` tinyint(1) NOT NULL DEFAULT '1',
  `criado_em` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `softwares`
--

LOCK TABLES `softwares` WRITE;
/*!40000 ALTER TABLE `softwares` DISABLE KEYS */;
INSERT INTO `softwares` VALUES (1,'Google Chrome','Navegador oficial do Google.','Navegador','bi-box-seam','https://www.google.com/chrome/',1,'2026-07-30 14:40:26'),(2,'Java',NULL,NULL,'bi-box-seam','https://www.java.com/pt-br/',1,'2026-08-04 11:24:25');
/*!40000 ALTER TABLE `softwares` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `usuario` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `senha_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `perfil` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ativo` tinyint(1) NOT NULL,
  `ultimo_login` datetime DEFAULT NULL,
  `criado_em` datetime NOT NULL,
  `atualizado_em` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_usuarios_email` (`email`),
  UNIQUE KEY `ix_usuarios_usuario` (`usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'Administrador','admin@portalti.local','admin','scrypt:32768:8:1$dJnWWbCRGO1e3DOd$47604c0f5f89396aa6247463a903aa75fd9454f770a3127e2376379cc0c3301245e7c1fcadd16bb86928333ce68a41b18b84a4f7dfc157db73eef698c3488079','administrador',1,'2026-08-05 18:26:58','2026-07-29 13:25:55','2026-08-05 18:26:58'),(2,'Richard','hugtak.richardalves@abrtelecom.com.br','richard alves','scrypt:32768:8:1$ImKfeWx5hBpsEDvd$ac440eb26d03023f0784c3925a5bf844bcf0f7d564999f71031fa41b2dc34703306c3e5704506f5d64cb522921505b411b18b464da153df565c16bcb6a1bd887','administrador',1,NULL,'2026-08-03 16:32:20','2026-08-03 16:32:20'),(3,'Helena','helenafurtado@hugtak.com','helena furtado','scrypt:32768:8:1$9ktjtL3XpUp26rPz$6d50121220ac2bc6c3a9fcfffd34dadae66aab6fc6f0719fa11701914c381df111bdab3a73eac1139c162bf8142e9b1251250786338006b9880a3072154c873d','administrador',1,NULL,'2026-08-03 16:34:27','2026-08-03 16:34:27'),(4,'Matheus Matias','matheusmatias.hugtak@abrtelecom.com.br','matias','scrypt:32768:8:1$P4yQBHzmqd5o5ZCW$05aa70e0a5c2e5c129b3b0c034cd3c445f54455b8a0d25882aa75076fa8b67281e5979a6d61c9bff3867ed8f04793043213da1f9e64b374a850325e2d69d2ec2','administrador',1,'2026-08-05 18:27:32','2026-08-03 16:36:01','2026-08-05 18:27:32'),(5,'Luiz Gustavo','luizgustavo.hugtak@abrtelecom.com.br','luiz','scrypt:32768:8:1$kwhA4Av96bVFkMkH$7ed600c8b7e11f5a0897e3fb0ae3c9cfd093d2f6e3dbb8fcae366a739f0b81685a338a2d75662350042bff6811a3de01715248365d0d2d67c56c69168f7af7a4','administrador',1,NULL,'2026-08-05 18:30:43','2026-08-05 18:30:43');
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

-- Dump completed on 2026-08-05 15:52:34
