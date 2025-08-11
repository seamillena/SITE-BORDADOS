CREATE DATABASE  IF NOT EXISTS `bordados_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `bordados_db`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: bordados_db
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `bordados`
--

DROP TABLE IF EXISTS `bordados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bordados` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) COLLATE utf8mb4_unicode_520_ci NOT NULL,
  `descricao` text COLLATE utf8mb4_unicode_520_ci,
  `imagem` varchar(255) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `imagens_extras` varchar(255) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `preco` decimal(10,2) NOT NULL DEFAULT '0.00',
  `temas` varchar(255) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `carrinho` varchar(10) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `quantidade` varchar(10) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `user_id` varchar(255) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bordados`
--

LOCK TABLES `bordados` WRITE;
/*!40000 ALTER TABLE `bordados` DISABLE KEYS */;
INSERT INTO `bordados` VALUES (1,'Porta-Alianças','18 cm, Laço para alianças, Arco de folhas, Arco de flores, Texto estilizado, Personalizado','porta_alianca.jpg','porta_alianca2.jpg, porta_alianca3.jpg, porta_alianca4.jpg, porta_alianca5.jpg',200.00,'Floral, Casamento','0','1',NULL),(2,'Retrato de Família','16 cm, Colorido, Desenho personalizado, Arco de flores, Bordado com fita','familia.jpg','familia2.jpg, familia3.jpg, familia4.jpg, familia5.jpg',250.00,'Retrato, Família, Floral','0','1',NULL),(3,'Retrato de Família','20 cm, Contorno apenas, Desenho personalizado, Arco de flores','nanda.jpg','nanda2.jpg, nanda3.jpg, nanda4.jpg, nanda5.jpg',250.00,'Retrato, Família, Floral','0','1',NULL),(4,'Retrato','16 cm, Colorido, Flores, Arco de Folhas, Pet não realista, Desenho personalizado, Bordado de fita','quezia.jpg','quezia2.jpg, quezia3.jpg, quezia4.jpg, quezia5.jpg',200.00,'Retrato, Pet, Floral','0','1',NULL),(5,'Retrato','22 cm, Colorido, Texto personalizado, Desenho personalizado, Arco de flores, Bordado de fita','nath.jpg','nath2.jpg, nath3.jpg, nath4.jpg, nath5.jpg',300.00,'Retrato, Família, Texto, Floral','0','1',NULL),(6,'Quarto infantil','22 cm, Texto estilizado personalizado, Desenho personalizado, Flores','quarto.jpg','quarto2.jpg, quarto3.jpg, quarto4.jpg, quarto5.jpg, quarto6.jpg',320.00,'Infantil, Desenho, Texto, Floral','0','1',NULL),(7,'Retrato','16 cm, Colorido, Desenho personalizado, Arco de folhas','casal1.jpg','casal2.jpg, casal3.jpg, casal4.jpg, casal5.jpg',250.00,'Retrato, Casal, Floral','0','1',NULL),(8,'Bordado de Família','20cm, Texto personalizado, Colorido, Desenho personalizado','pr.jpg','pr1.jpg,pr2.jpg,pr3.jpg',300.00,'Família, Texto','0','1',NULL),(9,'Comemoração de aprovação','20 cm, Colorido, Texto personalizado, Desenho personalizado','ufes.jpg','ufes2.jpg,ufes3.jpg,ufes4.jpg',300.00,'Família, Retrato, Texto','0','1',NULL),(10,'Família','16 cm, Desenho personalizado, Colorido','sorteio.jpg','sorteio2.jpg, sorteio3.jpg',230.00,'Família, Retrato','0','1',NULL),(11,'Porta Maternidade','22 cm, Texto estilizado personalizado, Desenho personalizado, Arco de folhas','aquilles.jpg','aquilles2.jpg,aquilles3.jpg,aquilles4.jpg,aquilles5.jpg',320.00,'Desenho, Infantil, Floral','0','1',NULL),(12,'Pet','22 cm, Preenchido em linhas, Texto estilizado personalizado, Desenho personalizado, Arco de folhas','zozo.jpg','zozo2.jpg,zozo3.jpg,zozo4.jpg,zozo5.jpg',400.00,'Gatinho, Pet, Floral','0','1',NULL),(13,'Casal','22 cm, Colorido, Desenho personalizado, Texto personalizado, Arco de flores','tais.jpg','tais2.jpg, tais3.jpg, tais4.jpg',350.00,'Casamento, Retrato, Texto, Floral, Casal','0','1',NULL),(14,'Retrato','18 cm, Colorido, Desenho personalizado, Texto estilizado personalizado','sunshine.jpg','sunshine2.jpg,sunshine3.jpg,sunshine4.jpg',230.00,'Retrato, Texto','0','1',NULL),(15,'Retrato','16 cm, Colorido, Desenho personalizado, Texto estilizado personalizado, Arco de flores, Flores','sogrei.jpg','sogrei2.jpg, sogrei3.jpg, sogrei4.jpg, sogrei5.jpg',250.00,'Retrato, Casamento, Floral, Família','0','1',NULL),(16,'Retrato','22 cm, Colorido, Texto estilizado personalizado, Desenho personalizado, Arco de folhas, Pet não realista','sara.jpg','sara2.jpg, sara3.jpg, sara4.jpg, sara5.jpg, sara6.jpg, sara7.jpg',330.00,'Retrato, Família, Pet, Floral','0','1',NULL),(17,'Casal','22 cm, Colorido, Texto personalizado, Desenho personalizado','rosa.jpg','',280.00,'Casamento, Retrato, Texto, Casal','0','1',NULL),(18,'Presépio','16 cm, Colorido, Laço natalino, Desenho personalizado','presepio.jpg','',180.00,'Desenho, Natal','0','1',NULL),(19,'Pet','22 cm, Preenchido em linhas, Texto estilizado personalizado, Desenho personalizado, Flores','bella.jpg','bella2.jpg,bella3.jpg,bella4.jpg,bella5.jpg',400.00,'Pet, Gatinho, Floral','0','1',NULL),(20,'Família','16 cm, Colorido, Arco de flores, Texto personalizado , Desenho personalizado','cecilia.jpg','cecilia2.jpg, cecilia3.jpg, cecilia4.jpg',220.00,'Retrato, Família, Texto, Floral','0','1',NULL),(21,'Pet','22 cm, Preenchido em linhas, Texto estilizado personalizado, Desenho personalizado, Flores','emma.jpg','emma2.jpg,emma3.jpg,emma4.jpg,emma5.jpg',450.00,'Pet, Cachorrinho ,Texto, Floral','0','1',NULL),(22,'Retrato','16 cm, Colorido, Texto estilizado personalizado, Desenho personalizado, Arco de flores','fernanda.jpg','fernanda2.jpg, fernanda3.jpg, fernanda4.jpg, fernanda5.jpg',220.00,'Retrato, Família, Floral','0','1',NULL),(23,'Retrato','22 cm, Colorido, Texto personalizado, Desenho personalizado, Arco de flores e folhas','ivone.jpg','ivone2.jpg, ivone3.jpg, ivone4.jpg, ivone5.jpg, ivone6.jpg',300.00,'Retrato, Família, Floral','0','1',NULL),(24,'Pet','22 cm, Preenchido em linhas, Texto estilizado personalizado, Desenho personalizado, Flores','izzie.jpg','izzie2.jpg, izzie3.jpg',450.00,'Cachorrinho, Pet, Texto, Floral','0','1',NULL),(25,'Família','22 cm, Pet não realista, Texto estilizado personalizado, Desenho personalizado','laisa.jpg','laisa2.jpg,laisa3.jpg,laisa4.jpg,laisa5.jpg',220.00,'Família, Desenho, Retrato, Pet','0','1',NULL),(26,'Desenho','22 cm, Desenho personalizado, Texto personalizado, Preenchido em linhas, Fundo colorido','lisa.jpg','lisa2.jpg,lisa3.jpg,lisa4.jpg,lisa5.jpg',220.00,'Desenho, Texto','0','1',NULL),(27,'Pet','22 cm, Preenchido em linhas, Texto estilizado personalizado, Desenho personalizado, Flores','luna.jpg','luna2.jpg,luna3.jpg,luna4.jpg,luna5.jpg',400.00,'Gatinho, Pet, Floral','0','1',NULL),(28,'Mapa','22 cm, Flores e folhagens, Texto personalizado, Desenho personalizado','mapa.jpg','mapa2.jpg,mapa3.jpg,mapa4.jpg,mapa5.jpg',180.00,'Desenho, Texto, Floral','0','1',NULL),(29,'Porta Maternidade','16 cm, Colorido, Texto estilizado personalizado, Desenho personalizado','miguel.jpg','miguel2.jpg,miguel3.jpg',250.00,'Infantil, Desenho, Texto','0','1',NULL),(30,'Logomarca','20 cm, Texto estilizado, Desenho personalizado','narri.jpg','narri2.jpg, narri3.jpg, narri4.jpg',170.00,'Desenho, Texto','0','1',NULL),(31,'Guirlanda','14 cm, Colorido, Texto estilizado personalizado, Flores','natal.jpg','',180.00,'Desenho, Natal, Texto','0','1',NULL);
/*!40000 ALTER TABLE `bordados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carrinhos`
--

DROP TABLE IF EXISTS `carrinhos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carrinhos` (
  `id_usuario` varchar(255) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `id_bordado` int DEFAULT NULL,
  `quantidade` int DEFAULT '1',
  `usuario` varchar(50) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  KEY `id_bordado` (`id_bordado`),
  CONSTRAINT `carrinhos_ibfk_1` FOREIGN KEY (`id_bordado`) REFERENCES `bordados` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carrinhos`
--

LOCK TABLES `carrinhos` WRITE;
/*!40000 ALTER TABLE `carrinhos` DISABLE KEYS */;
/*!40000 ALTER TABLE `carrinhos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comentarios`
--

DROP TABLE IF EXISTS `comentarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comentarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `publicacao` varchar(20) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `usuario` varchar(50) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `comentario` varchar(150) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `data_comentario` date DEFAULT NULL,
  `hora_comentario` time DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comentarios`
--

LOCK TABLES `comentarios` WRITE;
/*!40000 ALTER TABLE `comentarios` DISABLE KEYS */;
/*!40000 ALTER TABLE `comentarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contatos`
--

DROP TABLE IF EXISTS `contatos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contatos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `numero` varchar(50) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `insta` varchar(100) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contatos`
--

LOCK TABLES `contatos` WRITE;
/*!40000 ALTER TABLE `contatos` DISABLE KEYS */;
INSERT INTO `contatos` VALUES (1,'(27)99740-2134','oastronauta.bordados@outlook.com','@oastronauta.bordados');
/*!40000 ALTER TABLE `contatos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `curtidas`
--

DROP TABLE IF EXISTS `curtidas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `curtidas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario` varchar(100) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `publicacao` varchar(20) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `curtidas`
--

LOCK TABLES `curtidas` WRITE;
/*!40000 ALTER TABLE `curtidas` DISABLE KEYS */;
INSERT INTO `curtidas` VALUES (5,'administrador','PTLCGDYCQ3UX8MW'),(7,'seamillena','99WUCB7Q2RY479Z'),(9,'administrador','762RRON9PTDCRE7'),(10,'administrador','7NT2SW5RYEPG8M0'),(11,'seamillena','3ELVDRTE0K95KN8'),(13,'seamillena','X1G300SUGEQ7701'),(14,'seamillena','YC0TKR6785VVRG7'),(15,'administrador','GS9V7I9D6YHYZ13'),(16,'seamillena','7NT2SW5RYEPG8M0'),(17,'seamillena','GS9V7I9D6YHYZ13'),(18,'millena2','3U4F2CO0G2AG1DV'),(19,'administrador','W7EATD0UYBAY8VB'),(20,'administrador','MPJX9HKB31UBJ33');
/*!40000 ALTER TABLE `curtidas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `iniciodb`
--

DROP TABLE IF EXISTS `iniciodb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `iniciodb` (
  `imagens` varchar(255) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `textos` varchar(1000) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(255) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `iniciodb`
--

LOCK TABLES `iniciodb` WRITE;
/*!40000 ALTER TABLE `iniciodb` DISABLE KEYS */;
INSERT INTO `iniciodb` VALUES ('sogrei5.jpg','O bordado é uma das formas de arte têxtil mais antigas e encantadoras, capaz de transformar tecidos simples em peças únicas e cheias de significado. \r\nDesde tempos remotos, ele é utilizado para contar histórias, expressar criatividade e embelezar roupas, acessórios e decorações.',1,'O QUE É UM BORDADO'),('ivone6.jpg','O bordado não é apenas decorativo – ele tem múltiplas funções:\r\n✔ Decoração de Ambientes – Quadros bordados, almofadas, cortinas e toalhas de mesa trazem aconchego e estilo à casa.\r\n✔ Personalização de Roupas – Customiza peças básicas, como camisetas, jeans e casacos, dando um toque exclusivo.\r\n✔ Presentes Afetivos – Bordar nomes, datas ou mensagens em panos, toalhas e quadros cria lembranças emocionais.\r\n✔ Terapia e Relaxamento – O ato de bordar é uma atividade meditativa, que alivia o estresse e estimula a concentração.\r\n✔ Arte e Cultura – Muitos bordados carregam técnicas tradicionais, como o point de croix, o bordado livre e o rendendê, preservando saberes ancestrais.\r\n',2,'PARA QUE SERVEM OS BORDADOS'),('61ffa60daaab4e3791412d2e2db72ec21.jpg','O Astronauta Bordados surgiu durante a pandemia, em um período de recomeços e redescobertas. O que começou como um hobby para passar o tempo e aliviar a mente, logo se transformou em uma paixão. Entre linhas e bastidores, foram surgindo os primeiros bordados, feitos com carinho e sem grandes pretensões.\r\n\r\nCom o tempo, os amigos começaram a pedir peças personalizadas e o que era apenas um passatempo ganhou forma de projeto. O nome \"O Astronauta\" foi escolhido por representar a liberdade criativa e a vontade de explorar novos caminhos.\r\n\r\nDesde então, cada bordado carrega um pouco dessa história: o desejo de transformar momentos difíceis em arte, com cores, texturas e afeto.\r\n\r\n',3,'COMO SURGIU \"O ASTRONAUTA - BORDADOS\"'),('Imagem_do_WhatsApp_de_2025-06-16_as_20.33.34_14e5bbe3.jpg','Olá! Meu nome é Millena e sou a artesã por trás de O Astronauta Bordados. Comecei a bordar durante a pandemia, como uma forma de me conectar com algo feito à mão e cheio de significado.\r\n\r\nDesde então, o bordado se tornou parte da minha rotina e da minha expressão criativa. Cada peça que faço é pensada com carinho, buscando trazer cor e afeto para o dia a dia de quem recebe.\r\n\r\nAqui no site, você encontra um pouco dessa jornada, com um catálogo de bordados e a possibilidade de encomendar peças personalizadas. Obrigada por visitar!',4,'SOBRE A ARTESÃ');
/*!40000 ALTER TABLE `iniciodb` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mural`
--

DROP TABLE IF EXISTS `mural`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mural` (
  `publicacao` varchar(20) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `usuario` varchar(50) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `fotos` varchar(255) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `curtidas` int DEFAULT NULL,
  `legendas` varchar(500) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `data_publicacao` date DEFAULT NULL,
  `hora_publicacao` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mural`
--

LOCK TABLES `mural` WRITE;
/*!40000 ALTER TABLE `mural` DISABLE KEYS */;
INSERT INTO `mural` VALUES ('MPJX9HKB31UBJ33','administrador','mural_20250617182821_Imagem do WhatsApp de 2025-06-16 à(s) 20.24.44_4e6ea1ac.jpg',1,'daS','2025-06-17','18:28:22');
/*!40000 ALTER TABLE `mural` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos` (
  `fotos` varchar(1000) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `descricao` varchar(500) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `data_pedido` date DEFAULT NULL,
  `nome_cliente` varchar(100) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `tel_cliente` varchar(12) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `email_cliente` varchar(100) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `status_pedido` varchar(50) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `codigo_pedido` varchar(10) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `id_pedido` int NOT NULL AUTO_INCREMENT,
  `id_bordado` varchar(10) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `quantidade` int DEFAULT NULL,
  `usuario` varchar(100) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  PRIMARY KEY (`id_pedido`)
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
INSERT INTO `pedidos` VALUES (NULL,'Pedido Nathália - Venda','2025-06-10','Nathália','1','martins-millena@hotmail.com','Finalizado','I8DQE3KC9H',1,'1',1,NULL),(NULL,'Presente - Márcia e Rony','2025-06-10','Márcia e Rony','2','martins-millena@hotmail.com','Finalizado','ZB1C2U3PSJ',2,'2',1,NULL),(NULL,'Pedido Nandara - Venda','2025-06-10','Nandara','3','martins-millena@hotmail.com','Finalizado','6QQH2P9G92',3,'3',1,NULL),(NULL,'Pedido Quézia - Presente ','2025-06-10','Quézia','4','martins-millena@hotmail.com','Finalizado','EE2RSKLAHR',4,'4',1,NULL),(NULL,'Presente Nathália','2025-06-10','Nathália','5','martins-millena@hotmail.com','Finalizado','45XGPTJZ1O',5,'5',1,NULL),(NULL,'Pedido Nadine - Venda','2025-06-10','Nadine','6','martins-millena@hotmail.com','Finalizado','VMQPX6N1OS',6,'6',1,NULL),(NULL,'Pedido Nadine - Venda','2025-06-10','Nadine','7','martins-millena@hotmail.com','Finalizado','TK70WJWIMA',7,'7',1,NULL),(NULL,'Pedido Aline - Ministério da Mulher - Presente','2025-06-10','Aline','8','martins-millena@hotmail.com','Finalizado','M8ZOWYQINR',8,'8',1,NULL),(NULL,'Pedido Ivone - João - Venda','2025-06-10','Ivone','9','martins-millena@hotmail.com','Finalizado','UGZ04OHM82',9,'9',1,NULL),(NULL,'Sorteio - Orias Eduardo','2025-06-10','Orias','10','martins-millena@hotmail.com','Finalizado','0FUB4M7VVC',10,'10',1,NULL),(NULL,'Presente - Bruna Campista','2025-06-10','Bruna','11','martins-millena@hotmail.com','Finalizado','853DSHZZK8',11,'11',1,NULL),(NULL,'Presente - Tia Márcia','2025-06-10','Márcia','12','martins-millena@hotmail.com','Finalizado','MMUXL9RMLR',12,'12',1,NULL),(NULL,'Presente - Taís','2025-06-10','Taís','13','martins-millena@hotmail.com','Finalizado','94CHNU01QA',13,'13',1,NULL),(NULL,'Presente - Sunshine','2025-06-10','Sunshine','14','martins-millena@hotmail.com','Finalizado','7SN0UFB921',14,'14',1,NULL),(NULL,'Pedido - Tia Ene - Permuta','2025-06-10','Luciene','15','martins-millena@hotmail.com','Finalizado','BMFY0KQ7J5',15,'15',1,NULL),(NULL,'Pedido - Tia Sara - Presente','2025-06-10','Sara','16','martins-millena@hotmail.com','Finalizado','F41PMXFP79',16,'16',1,NULL),(NULL,'Pedido - Rosa - Presente','2025-06-10','Rosa','17','martins-millena@hotmail.com','Finalizado','PHJZ09CKRA',17,'17',1,NULL),(NULL,'Sorteio - Camila','2025-06-10','Camila','18','martins-millena@hotmail.com','Finalizado','VAAQTEZZIQ',18,'18',1,NULL),(NULL,'Presente - Tia Márcia','2025-06-10','Márcia','19','martins-millena@hotmail.com','Finalizado','63J33MCECH',19,'19',1,NULL),(NULL,'Presente - Cecília, Camila e Gleydson','2025-06-10','Cecília','20','martins-millena@hotmail.com','Finalizado','RB0K0Y2F1M',20,'20',1,NULL),(NULL,'Presente - Tia Márcia','2025-06-10','Márcia','21','martins-millena@hotmail.com','Finalizado','U1X6IZEGMO',21,'21',1,NULL),(NULL,'Pedido - Fernanda - Presente','2025-06-10','Fernanda','22','martins-millena@hotmail.com','Finalizado','6Z3WN9X0Y5',22,'22',1,NULL),(NULL,'Pedido - Ivone - Venda','2025-06-10','Ivone','23','martins-millena@hotmail.com','Finalizado','D10DIH8Y34',23,'23',1,NULL),(NULL,'Presente - Tia Márcia','2025-06-10','Márcia','24','martins-millena@hotmail.com','Finalizado','JO04M0I19I',24,'24',1,NULL),(NULL,'Presente - Laisa','2025-06-10','Laisa','25','martins-millena@hotmail.com','Finalizado','ORMGTU01GZ',25,'25',1,NULL),(NULL,'Bordado Lisa - Não vendido','2025-06-10','Millena','26','martins-millena@hotmail.com','Finalizado','IHRNMLNULP',26,'26',1,NULL),(NULL,'Presente - Tia Márcia','2025-06-10','Márcia','27','martins-millena@hotmail.com','Finalizado','WUKKH4PXE7',27,'27',1,NULL),(NULL,'Presente - Laisa','2025-06-10','Laisa','28','martins-millena@hotmail.com','Finalizado','FSGGZDM750',28,'28',1,NULL),(NULL,'Presente - Taty e Esley','2025-06-10','Taty e Esley','29','martins-millena@hotmail.com','Finalizado','4QOWMJ6LAB',29,'29',1,NULL),(NULL,'Pedido - Narri - Venda','2025-06-10','Narri','30','martins-millena@hotmail.com','Finalizado','GI9PFC7IXA',30,'30',1,NULL),(NULL,'Sorteio - Luciene','2025-06-10','Luciene','31','martins-millena@hotmail.com','Finalizado','TJLIPUWVLR',31,'31',1,NULL);
/*!40000 ALTER TABLE `pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `senha` varchar(100) COLLATE utf8mb4_unicode_520_ci NOT NULL,
  `foto` varchar(255) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `nome` varchar(255) COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '',
  `sobrenome` varchar(255) COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '',
  `usuario` varchar(50) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `tipo` varchar(50) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `telefone` varchar(15) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'autorizarlogin','61ffa60daaab4e3791412d2e2db72ec21.jpg','O ASTRONAUTA','BORDADOS','administrador','administrador',NULL,NULL),(13,'administrador',NULL,'O ASTRONAUTA','BORDADOS','oastronauta.bordados','administrador','oastronauta.bordados@outlook.com','2799709492'),(15,'seamillena',NULL,'Millena','Martins','seamillena','cliente','seamillena@gmail.com','27997402134');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'bordados_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-17 18:38:38
