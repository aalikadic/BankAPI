-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: testprojectdatabase
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
-- Table structure for table `credittable`
--

DROP TABLE IF EXISTS `credittable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `credittable` (
  `Id` bigint NOT NULL AUTO_INCREMENT,
  `AccountId` bigint NOT NULL,
  `CustomerId` bigint NOT NULL,
  `TotalCreditAmount` decimal(10,0) NOT NULL,
  `CreditIssueDate` date NOT NULL,
  `ToBePaidBefore` date NOT NULL,
  `IsPaidOff` binary(1) NOT NULL DEFAULT '0',
  `IsOverdue` binary(1) NOT NULL DEFAULT '0',
  `RemainingAmountToBePaid` decimal(10,0) NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `AccountId` (`AccountId`),
  KEY `credittable_ibfk_2_idx` (`CustomerId`),
  CONSTRAINT `credittable_ibfk_1` FOREIGN KEY (`AccountId`) REFERENCES `accounttable` (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `credittable`
--

LOCK TABLES `credittable` WRITE;
/*!40000 ALTER TABLE `credittable` DISABLE KEYS */;
INSERT INTO `credittable` VALUES (6,1,0,10,'2020-08-09','2020-08-19',_binary '1',_binary '0',6),(7,1,0,10,'2020-08-09','2020-08-19',_binary '0',_binary '0',10),(8,1,0,10,'2020-08-09','2020-08-19',_binary '0',_binary '0',10),(9,1,0,10,'2020-08-09','2020-08-19',_binary '0',_binary '0',10),(13,1,0,10,'2020-08-09','2020-08-19',_binary '0',_binary '0',10),(14,1,0,10,'2020-08-09','2020-08-19',_binary '0',_binary '0',10),(15,1,0,10,'2020-08-09','2020-08-19',_binary '0',_binary '0',10),(16,1,0,10,'2020-08-09','2020-08-19',_binary '0',_binary '0',10),(17,1,0,10,'2020-08-09','2020-08-19',_binary '0',_binary '0',10);
/*!40000 ALTER TABLE `credittable` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-08-10  2:06:25
