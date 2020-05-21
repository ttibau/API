-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: modulelift
-- ------------------------------------------------------
-- Server version	8.0.19

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
-- Dumping data for table `api_keys`
--

LOCK TABLES `api_keys` WRITE;
/*!40000 ALTER TABLE `api_keys` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_keys` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `api_paths`
--

LOCK TABLES `api_paths` WRITE;
/*!40000 ALTER TABLE `api_paths` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_paths` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `api_permissions`
--

LOCK TABLES `api_permissions` WRITE;
/*!40000 ALTER TABLE `api_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `elo_settings`
--

LOCK TABLES `elo_settings` WRITE;
/*!40000 ALTER TABLE `elo_settings` DISABLE KEYS */;
INSERT INTO `elo_settings` VALUES (1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `elo_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ip_details`
--

LOCK TABLES `ip_details` WRITE;
/*!40000 ALTER TABLE `ip_details` DISABLE KEYS */;
INSERT INTO `ip_details` VALUES ('122.0.0.0',0,'Spark New Zealand Trading Ltd','Christchurch','New Zealand');
/*!40000 ALTER TABLE `ip_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `league_admins`
--

LOCK TABLES `league_admins` WRITE;
/*!40000 ALTER TABLE `league_admins` DISABLE KEYS */;
/*!40000 ALTER TABLE `league_admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `league_info`
--

LOCK TABLES `league_info` WRITE;
/*!40000 ALTER TABLE `league_info` DISABLE KEYS */;
INSERT INTO `league_info` VALUES ('tl','Test League','http://localhost:8888',NULL,NULL,2,'?','Test League',0,0,0,1,360,1);
/*!40000 ALTER TABLE `league_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `map_pool`
--

LOCK TABLES `map_pool` WRITE;
/*!40000 ALTER TABLE `map_pool` DISABLE KEYS */;
/*!40000 ALTER TABLE `map_pool` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `regions`
--

LOCK TABLES `regions` WRITE;
/*!40000 ALTER TABLE `regions` DISABLE KEYS */;
INSERT INTO `regions` VALUES ('OCE');
/*!40000 ALTER TABLE `regions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `scoreboard`
--

LOCK TABLES `scoreboard` WRITE;
/*!40000 ALTER TABLE `scoreboard` DISABLE KEYS */;
/*!40000 ALTER TABLE `scoreboard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `scoreboard_total`
--

LOCK TABLES `scoreboard_total` WRITE;
/*!40000 ALTER TABLE `scoreboard_total` DISABLE KEYS */;
/*!40000 ALTER TABLE `scoreboard_total` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `statistics`
--

LOCK TABLES `statistics` WRITE;
/*!40000 ALTER TABLE `statistics` DISABLE KEYS */;
/*!40000 ALTER TABLE `statistics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('fffe46cd-6668-45a1-817c-e18d8cafae23','76561198077228213',329584121472876554,'jpeg','Ward','2020-05-21 04:12:50','122.0.0.0'),('fffe46cd-6668-45a1-817c-e18d8cafae24','76561198165366861',181715064640897024,'jpeg','Ensyy','2020-05-21 04:13:29','122.0.0.0'),('fffe46cd-6668-45a1-817c-e18d8cafae25','78435584216936448',78435584216936448,'jpeg','Lubricant Jam','2020-05-21 04:14:03','122.0.0.0'),('fffe46cd-6668-45a1-817c-e18d8cafae26','76561198139510215',157278154631806976,'jpeg','Y-Fu','2020-05-21 04:14:30','122.0.0.0'),('fffe46cd-6668-45a1-817c-e18d8cafae27','76561198017567105',163076343448338432,'jpeg','Dave','2020-05-21 04:15:04','122.0.0.0'),('fffe46cd-6668-45a1-817c-e18d8cafae28','76561198326361803',206640791584505856,'jpeg','Aiden','2020-05-21 04:15:37','122.0.0.0'),('fffe46cd-6668-45a1-817c-e18d8cafae29','76561198165844676',181627980739641354,'jpeg','Bez','2020-05-21 04:16:01','122.0.0.0'),('fffe46cd-6668-45a1-817c-e18d8cafae30','76561198838077439',195530068947107840,'jpeg','Brad','2020-05-21 04:16:51','122.0.0.0'),('fffe46cd-6668-45a1-817c-e18d8cafae31','76561198066265095',221882886842875905,'jpeg','Nick0Lite','2020-05-21 04:17:13','122.0.0.0'),('fffe46cd-6668-45a1-817c-e18d8cafae32','76561198332393913',473354482915475457,'jpeg','Doug','2020-05-21 04:17:39','122.0.0.0');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-21 16:47:24
