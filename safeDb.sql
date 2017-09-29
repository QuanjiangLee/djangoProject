-- MySQL dump 10.13  Distrib 5.7.11, for Linux (x86_64)
--
-- Host: localhost    Database: sss
-- ------------------------------------------------------
-- Server version	5.7.11

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `adminLogin`
--

DROP TABLE IF EXISTS `adminLogin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `adminLogin` (
  `loginAcc` varchar(50) NOT NULL,
  `LoginTime` datetime NOT NULL,
  PRIMARY KEY (`loginAcc`),
  CONSTRAINT `adminLogin_ibfk_1` FOREIGN KEY (`loginAcc`) REFERENCES `loginInf` (`loginAcc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adminLogin`
--

LOCK TABLES `adminLogin` WRITE;
/*!40000 ALTER TABLE `adminLogin` DISABLE KEYS */;
/*!40000 ALTER TABLE `adminLogin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alterHostIp`
--

DROP TABLE IF EXISTS `alterHostIp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alterHostIp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `newIp` varchar(40) DEFAULT NULL,
  `oldIp` varchar(40) DEFAULT NULL,
  `alterTime` datetime NOT NULL,
  `newIpExplain` text,
  `oldIpExplain` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alterHostIp`
--

LOCK TABLES `alterHostIp` WRITE;
/*!40000 ALTER TABLE `alterHostIp` DISABLE KEYS */;
/*!40000 ALTER TABLE `alterHostIp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alterKeywords`
--

DROP TABLE IF EXISTS `alterKeywords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alterKeywords` (
  `alterId` int(11) NOT NULL,
  `userId` int(11) NOT NULL,
  `fileHash` char(32) NOT NULL,
  PRIMARY KEY (`alterId`),
  KEY `fileHash` (`fileHash`),
  CONSTRAINT `alterKeywords_ibfk_1` FOREIGN KEY (`fileHash`) REFERENCES `fileInf` (`fileHash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alterKeywords`
--

LOCK TABLES `alterKeywords` WRITE;
/*!40000 ALTER TABLE `alterKeywords` DISABLE KEYS */;
/*!40000 ALTER TABLE `alterKeywords` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alterMAC`
--

DROP TABLE IF EXISTS `alterMAC`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alterMAC` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `newMAC` varchar(20) DEFAULT NULL,
  `oldMAC` varchar(20) DEFAULT NULL,
  `alterTime` datetime NOT NULL,
  `newMACExplain` text,
  `oldMACExplain` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alterMAC`
--

LOCK TABLES `alterMAC` WRITE;
/*!40000 ALTER TABLE `alterMAC` DISABLE KEYS */;
/*!40000 ALTER TABLE `alterMAC` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `computerInf`
--

DROP TABLE IF EXISTS `computerInf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `computerInf` (
  `hostHD` varchar(40) NOT NULL,
  `hostMac` varchar(64) NOT NULL,
  `hostName` varchar(255) DEFAULT NULL,
  `sysversion` varchar(255) DEFAULT NULL,
  `sysName` varchar(255) DEFAULT NULL,
  `userId` int(11) NOT NULL,
  `userIp` varchar(40) DEFAULT NULL,
  `userNetStatus` int(11) NOT NULL DEFAULT '0',
  `userScanStatus` int(11) NOT NULL DEFAULT '0',
  `sysType` int(4) DEFAULT NULL,
  `sysTextEditor` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`userId`),
  KEY `userId` (`userId`),
  CONSTRAINT `computerInf_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `userInf` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `computerInf`
--

LOCK TABLES `computerInf` WRITE;
/*!40000 ALTER TABLE `computerInf` DISABLE KEYS */;
/*!40000 ALTER TABLE `computerInf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dbBackInf`
--

DROP TABLE IF EXISTS `dbBackInf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dbBackInf` (
  `dbId` int(11) NOT NULL AUTO_INCREMENT,
  `dbName` varchar(255) NOT NULL DEFAULT '自动备份',
  `local_file` varchar(255) DEFAULT NULL,
  `dbTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dbRemark` text,
  `userAcc` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`dbId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dbBackInf`
--

LOCK TABLES `dbBackInf` WRITE;
/*!40000 ALTER TABLE `dbBackInf` DISABLE KEYS */;
/*!40000 ALTER TABLE `dbBackInf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `depaertRoleInf`
--

DROP TABLE IF EXISTS `depaertRoleInf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `depaertRoleInf` (
  `deparmentId` int(11) NOT NULL,
  `roleId` int(11) NOT NULL,
  PRIMARY KEY (`deparmentId`,`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `depaertRoleInf`
--

LOCK TABLES `depaertRoleInf` WRITE;
/*!40000 ALTER TABLE `depaertRoleInf` DISABLE KEYS */;
/*!40000 ALTER TABLE `depaertRoleInf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departmentInf`
--

DROP TABLE IF EXISTS `departmentInf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `departmentInf` (
  `departmentId` int(11) NOT NULL AUTO_INCREMENT,
  `departmentName` varchar(255) NOT NULL,
  `departmentPeoNum` int(11) NOT NULL DEFAULT '0',
  `departmentStatus` int(11) NOT NULL DEFAULT '1',
  `departmentExplian` text,
  `keyPath` varchar(255) NOT NULL DEFAULT 'null',
  `userLoginStatus` int(11) NOT NULL DEFAULT '0',
  `province` varchar(50) NOT NULL DEFAULT '当前级别',
  `city` varchar(50) NOT NULL,
  `createTime` datetime NOT NULL DEFAULT '1700-00-00 00:00:00',
  `createUser` varchar(255) NOT NULL,
  `status` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`departmentId`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departmentInf`
--

LOCK TABLES `departmentInf` WRITE;
/*!40000 ALTER TABLE `departmentInf` DISABLE KEYS */;
INSERT INTO `departmentInf` VALUES (1,'三级部门',0,1,NULL,'/tmp/SafeDir',0,'一级部门','二级部门','2017-09-29 22:25:31','一级部门:二级部门:三级部门:超超管',0),(2,'三级部门',0,1,NULL,'/tmp/SafeDir',0,'陕西省','二级部门','2017-09-29 22:25:31','一级部门:二级部门:三级部门:超超管',0),(3,'三级部门',0,1,NULL,'/tmp/SafeDir',0,'陕西省','公安厅','2017-09-29 22:25:31','一级部门:二级部门:三级部门:超超管',0),(4,'资料处',0,1,NULL,'/tmp/SafeDir',0,'陕西省','公安厅','2017-09-29 22:25:31','一级部门:二级部门:三级部门:超超管',0);
/*!40000 ALTER TABLE `departmentInf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departmentKey`
--

DROP TABLE IF EXISTS `departmentKey`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `departmentKey` (
  `keyId` int(11) NOT NULL,
  `departmentId` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`keyId`,`departmentId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departmentKey`
--

LOCK TABLES `departmentKey` WRITE;
/*!40000 ALTER TABLE `departmentKey` DISABLE KEYS */;
/*!40000 ALTER TABLE `departmentKey` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fileInf`
--

DROP TABLE IF EXISTS `fileInf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fileInf` (
  `fileHash` char(32) NOT NULL,
  `fileLocalName` varchar(255) NOT NULL,
  `filePath` varchar(255) NOT NULL,
  `fileSize` int(11) NOT NULL,
  `filePasswd` text,
  PRIMARY KEY (`fileHash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fileInf`
--

LOCK TABLES `fileInf` WRITE;
/*!40000 ALTER TABLE `fileInf` DISABLE KEYS */;
/*!40000 ALTER TABLE `fileInf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `filePasswdInf`
--

DROP TABLE IF EXISTS `filePasswdInf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `filePasswdInf` (
  `passwdId` int(11) NOT NULL,
  `passwdPath` varchar(255) NOT NULL,
  `passwdfileName` varchar(255) NOT NULL,
  PRIMARY KEY (`passwdId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filePasswdInf`
--

LOCK TABLES `filePasswdInf` WRITE;
/*!40000 ALTER TABLE `filePasswdInf` DISABLE KEYS */;
/*!40000 ALTER TABLE `filePasswdInf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `filePasswdLog`
--

DROP TABLE IF EXISTS `filePasswdLog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `filePasswdLog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `alterTime` datetime NOT NULL,
  `passwdId` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `passwdId` (`passwdId`),
  CONSTRAINT `filePasswdLog_ibfk_1` FOREIGN KEY (`passwdId`) REFERENCES `filePasswdInf` (`passwdId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filePasswdLog`
--

LOCK TABLES `filePasswdLog` WRITE;
/*!40000 ALTER TABLE `filePasswdLog` DISABLE KEYS */;
/*!40000 ALTER TABLE `filePasswdLog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fileUploadInf`
--

DROP TABLE IF EXISTS `fileUploadInf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fileUploadInf` (
  `UploadId` int(11) NOT NULL AUTO_INCREMENT,
  `userId` int(11) NOT NULL,
  `fileHash` char(32) NOT NULL,
  `fileName` varchar(255) NOT NULL,
  `uploadTime` datetime NOT NULL,
  `errId` int(11) DEFAULT NULL,
  PRIMARY KEY (`UploadId`),
  KEY `userId` (`userId`),
  KEY `fileHash` (`fileHash`),
  CONSTRAINT `fileUploadInf_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `userInf` (`userId`),
  CONSTRAINT `fileUploadInf_ibfk_2` FOREIGN KEY (`fileHash`) REFERENCES `fileInf` (`fileHash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fileUploadInf`
--

LOCK TABLES `fileUploadInf` WRITE;
/*!40000 ALTER TABLE `fileUploadInf` DISABLE KEYS */;
/*!40000 ALTER TABLE `fileUploadInf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `keywordsInf`
--

DROP TABLE IF EXISTS `keywordsInf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `keywordsInf` (
  `keyId` int(11) NOT NULL AUTO_INCREMENT,
  `keyword` varchar(50) NOT NULL,
  `keyLever` int(11) NOT NULL DEFAULT '0',
  `createUserStatus` int(11) NOT NULL DEFAULT '0',
  `createUserId` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`keyId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `keywordsInf`
--

LOCK TABLES `keywordsInf` WRITE;
/*!40000 ALTER TABLE `keywordsInf` DISABLE KEYS */;
/*!40000 ALTER TABLE `keywordsInf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log`
--

DROP TABLE IF EXISTS `log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log` (
  `logId` int(11) NOT NULL AUTO_INCREMENT,
  `logUpTime` datetime NOT NULL,
  `dataError` varchar(255) DEFAULT NULL,
  `userId` int(11) NOT NULL,
  `logStatus` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`logId`),
  KEY `userId` (`userId`),
  CONSTRAINT `log_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `userInf` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log`
--

LOCK TABLES `log` WRITE;
/*!40000 ALTER TABLE `log` DISABLE KEYS */;
/*!40000 ALTER TABLE `log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loginInf`
--

DROP TABLE IF EXISTS `loginInf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `loginInf` (
  `loginAcc` varchar(50) NOT NULL,
  `loginName` varchar(255) DEFAULT NULL,
  `loginPasswd` varchar(20) NOT NULL DEFAULT '123456',
  `loginStatus` int(11) NOT NULL DEFAULT '1',
  `userId` int(11) NOT NULL,
  `isSuperAdmin` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`loginAcc`),
  KEY `userId` (`userId`),
  CONSTRAINT `loginInf_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `userInf` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loginInf`
--

LOCK TABLES `loginInf` WRITE;
/*!40000 ALTER TABLE `loginInf` DISABLE KEYS */;
/*!40000 ALTER TABLE `loginInf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loginLog`
--

DROP TABLE IF EXISTS `loginLog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `loginLog` (
  `Lid` int(11) NOT NULL AUTO_INCREMENT,
  `userId` int(11) NOT NULL,
  `ltime` datetime NOT NULL,
  `lhostIp` varchar(50) DEFAULT NULL,
  `lstatus` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`Lid`),
  KEY `userId` (`userId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loginLog`
--

LOCK TABLES `loginLog` WRITE;
/*!40000 ALTER TABLE `loginLog` DISABLE KEYS */;
/*!40000 ALTER TABLE `loginLog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `noticeData`
--

DROP TABLE IF EXISTS `noticeData`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `noticeData` (
  `Nid` int(11) NOT NULL AUTO_INCREMENT,
  `Ntime` datetime NOT NULL DEFAULT '1990-01-01 00:00:00',
  `Ntitle` varchar(255) NOT NULL DEFAULT 'null',
  `Nbody` text NOT NULL,
  `Nstatus` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`Nid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `noticeData`
--

LOCK TABLES `noticeData` WRITE;
/*!40000 ALTER TABLE `noticeData` DISABLE KEYS */;
/*!40000 ALTER TABLE `noticeData` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `portInf`
--

DROP TABLE IF EXISTS `portInf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `portInf` (
  `port` int(11) NOT NULL,
  `PortExplan` text,
  PRIMARY KEY (`port`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `portInf`
--

LOCK TABLES `portInf` WRITE;
/*!40000 ALTER TABLE `portInf` DISABLE KEYS */;
/*!40000 ALTER TABLE `portInf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `powerInf`
--

DROP TABLE IF EXISTS `powerInf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `powerInf` (
  `powerId` int(11) NOT NULL AUTO_INCREMENT,
  `powerName` varchar(255) NOT NULL,
  `powerExplan` text NOT NULL,
  `PowerStatus` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`powerId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `powerInf`
--

LOCK TABLES `powerInf` WRITE;
/*!40000 ALTER TABLE `powerInf` DISABLE KEYS */;
/*!40000 ALTER TABLE `powerInf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `remoteRecord`
--

DROP TABLE IF EXISTS `remoteRecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `remoteRecord` (
  `rrId` int(11) NOT NULL AUTO_INCREMENT,
  `sendNo` varchar(50) NOT NULL,
  `receiveNo` varchar(50) NOT NULL,
  `orderName` varchar(255) DEFAULT NULL,
  `sendTime` datetime DEFAULT NULL,
  `overTime` datetime DEFAULT NULL,
  `sendStatus` int(11) NOT NULL DEFAULT '0',
  `handleStatus` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`rrId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `remoteRecord`
--

LOCK TABLES `remoteRecord` WRITE;
/*!40000 ALTER TABLE `remoteRecord` DISABLE KEYS */;
/*!40000 ALTER TABLE `remoteRecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roleInf`
--

DROP TABLE IF EXISTS `roleInf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roleInf` (
  `roleId` int(11) NOT NULL AUTO_INCREMENT,
  `roleName` varchar(255) NOT NULL,
  `rolePNum` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roleInf`
--

LOCK TABLES `roleInf` WRITE;
/*!40000 ALTER TABLE `roleInf` DISABLE KEYS */;
/*!40000 ALTER TABLE `roleInf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rolePower`
--

DROP TABLE IF EXISTS `rolePower`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rolePower` (
  `roleId` int(11) NOT NULL,
  `powerId` int(11) NOT NULL,
  PRIMARY KEY (`roleId`,`powerId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rolePower`
--

LOCK TABLES `rolePower` WRITE;
/*!40000 ALTER TABLE `rolePower` DISABLE KEYS */;
/*!40000 ALTER TABLE `rolePower` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `secondScan`
--

DROP TABLE IF EXISTS `secondScan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `secondScan` (
  `ssId` int(11) NOT NULL AUTO_INCREMENT,
  `fileName` varchar(255) DEFAULT NULL,
  `filePath` varchar(255) DEFAULT NULL,
  `keywords` varchar(255) DEFAULT NULL,
  `scanTime` datetime DEFAULT NULL,
  `userNo` varchar(50) DEFAULT NULL,
  `userId` int(11) DEFAULT NULL,
  `keyExtend` varchar(255) DEFAULT NULL,
  `fileHash` char(32) DEFAULT NULL,
  `uploadStatus` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ssId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `secondScan`
--

LOCK TABLES `secondScan` WRITE;
/*!40000 ALTER TABLE `secondScan` DISABLE KEYS */;
/*!40000 ALTER TABLE `secondScan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `selectCode`
--

DROP TABLE IF EXISTS `selectCode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `selectCode` (
  `selectId` int(11) NOT NULL AUTO_INCREMENT,
  `selectTitle` varchar(255) NOT NULL,
  `selectBody` text,
  `selectStatus` int(11) NOT NULL DEFAULT '1',
  `selectExplain` text,
  PRIMARY KEY (`selectId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `selectCode`
--

LOCK TABLES `selectCode` WRITE;
/*!40000 ALTER TABLE `selectCode` DISABLE KEYS */;
/*!40000 ALTER TABLE `selectCode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `selfCheck`
--

DROP TABLE IF EXISTS `selfCheck`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `selfCheck` (
  `usId` int(11) NOT NULL AUTO_INCREMENT,
  `userId` int(11) NOT NULL,
  `fileName` varchar(255) DEFAULT NULL,
  `filePath` varchar(255) DEFAULT NULL,
  `keywords` varchar(255) DEFAULT NULL,
  `keyExtend` varchar(255) DEFAULT NULL,
  `scanTime` datetime DEFAULT NULL,
  `fileHash` char(32) CHARACTER SET latin1 DEFAULT NULL,
  PRIMARY KEY (`usId`),
  KEY `tem_userscan` (`userId`),
  CONSTRAINT `tem_userscan` FOREIGN KEY (`userId`) REFERENCES `userInf` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `selfCheck`
--

LOCK TABLES `selfCheck` WRITE;
/*!40000 ALTER TABLE `selfCheck` DISABLE KEYS */;
/*!40000 ALTER TABLE `selfCheck` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `selfKeywords`
--

DROP TABLE IF EXISTS `selfKeywords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `selfKeywords` (
  `keyId` int(11) NOT NULL AUTO_INCREMENT,
  `keyword` varchar(50) NOT NULL,
  `userId` varchar(50) DEFAULT NULL,
  `keyLever` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`keyId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `selfKeywords`
--

LOCK TABLES `selfKeywords` WRITE;
/*!40000 ALTER TABLE `selfKeywords` DISABLE KEYS */;
/*!40000 ALTER TABLE `selfKeywords` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ukeyInf`
--

DROP TABLE IF EXISTS `ukeyInf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ukeyInf` (
  `ukId` int(11) NOT NULL AUTO_INCREMENT,
  `companyName` varchar(255) NOT NULL,
  `userScale` int(11) NOT NULL,
  `installNum` int(11) DEFAULT NULL,
  `serviceUntilTime` datetime NOT NULL,
  `isGranted` char(13) NOT NULL,
  PRIMARY KEY (`ukId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ukeyInf`
--

LOCK TABLES `ukeyInf` WRITE;
/*!40000 ALTER TABLE `ukeyInf` DISABLE KEYS */;
/*!40000 ALTER TABLE `ukeyInf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userErrInf`
--

DROP TABLE IF EXISTS `userErrInf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userErrInf` (
  `errId` int(11) NOT NULL AUTO_INCREMENT,
  `userId` int(11) NOT NULL,
  `errTime` datetime NOT NULL,
  `fileHash` char(32) NOT NULL,
  `errOperate` varchar(255) DEFAULT NULL,
  `keyWords` text,
  `hostIP` varchar(50) DEFAULT NULL,
  `errStatus` int(11) NOT NULL DEFAULT '0',
  `errCode` int(11) NOT NULL DEFAULT '0',
  `keyExtend` varchar(255) DEFAULT NULL,
  `fileName` varchar(255) NOT NULL,
  PRIMARY KEY (`errId`),
  KEY `fileHash` (`fileHash`),
  KEY `userId` (`userId`),
  KEY `errTime` (`errTime`),
  CONSTRAINT `userErrInf_ibfk_2` FOREIGN KEY (`userId`) REFERENCES `userInf` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userErrInf`
--

LOCK TABLES `userErrInf` WRITE;
/*!40000 ALTER TABLE `userErrInf` DISABLE KEYS */;
/*!40000 ALTER TABLE `userErrInf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userInf`
--

DROP TABLE IF EXISTS `userInf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userInf` (
  `userId` int(11) NOT NULL AUTO_INCREMENT,
  `userNo` varchar(30) NOT NULL,
  `userName` varchar(40) NOT NULL,
  `userSex` varchar(10) NOT NULL DEFAULT 'null',
  `userTel` varchar(11) NOT NULL DEFAULT 'null',
  `userPosition` varchar(100) NOT NULL DEFAULT 'null',
  `userStatus` int(11) NOT NULL DEFAULT '1',
  `registStatus` int(2) NOT NULL DEFAULT '0',
  `loginStatus` int(2) NOT NULL DEFAULT '0',
  `userIdentify` varchar(20) NOT NULL DEFAULT 'null',
  `departmentId` int(11) NOT NULL,
  `userLever` varchar(50) NOT NULL DEFAULT 'null',
  `userPasswd` varchar(255) NOT NULL DEFAULT '*6A7A490FB9DC8C33C2B025A91737077A7E9CC5E5',
  `userPositionStatus` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`userId`),
  UNIQUE KEY `userNo` (`userNo`),
  KEY `userNo_2` (`userNo`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userInf`
--

LOCK TABLES `userInf` WRITE;
/*!40000 ALTER TABLE `userInf` DISABLE KEYS */;
INSERT INTO `userInf` VALUES (1,'1234567','超高管','null','null','超高管',1,0,0,'null',1,'null','*6A7A490FB9DC8C33C2B025A91737077A7E9CC5E5',2),(2,'1234568','超管','null','null','超管',1,0,0,'null',2,'null','*6A7A490FB9DC8C33C2B025A91737077A7E9CC5E5',2),(3,'1234569','普管','null','null','普管',1,0,0,'null',3,'null','*6A7A490FB9DC8C33C2B025A91737077A7E9CC5E5',1),(4,'1234570','一般人','null','null','一般人',1,0,0,'null',4,'null','*6A7A490FB9DC8C33C2B025A91737077A7E9CC5E5',0);
/*!40000 ALTER TABLE `userInf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userPowerInf`
--

DROP TABLE IF EXISTS `userPowerInf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userPowerInf` (
  `userId` int(11) NOT NULL,
  `powerId` int(11) NOT NULL,
  PRIMARY KEY (`userId`,`powerId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userPowerInf`
--

LOCK TABLES `userPowerInf` WRITE;
/*!40000 ALTER TABLE `userPowerInf` DISABLE KEYS */;
/*!40000 ALTER TABLE `userPowerInf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userRoleInf`
--

DROP TABLE IF EXISTS `userRoleInf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userRoleInf` (
  `userId` int(11) NOT NULL,
  `roleId` int(11) NOT NULL,
  PRIMARY KEY (`userId`,`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userRoleInf`
--

LOCK TABLES `userRoleInf` WRITE;
/*!40000 ALTER TABLE `userRoleInf` DISABLE KEYS */;
/*!40000 ALTER TABLE `userRoleInf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userScan`
--

DROP TABLE IF EXISTS `userScan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userScan` (
  `usId` int(11) NOT NULL AUTO_INCREMENT,
  `fileName` varchar(255) DEFAULT NULL,
  `filePath` varchar(255) DEFAULT NULL,
  `keywords` varchar(255) DEFAULT NULL,
  `scanTime` datetime DEFAULT NULL,
  `userNo` varchar(50) DEFAULT NULL,
  `userId` int(11) DEFAULT NULL,
  `keyExtend` varchar(255) DEFAULT NULL,
  `fileHash` char(32) DEFAULT NULL,
  `uploadStatus` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`usId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userScan`
--

LOCK TABLES `userScan` WRITE;
/*!40000 ALTER TABLE `userScan` DISABLE KEYS */;
/*!40000 ALTER TABLE `userScan` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-09-29 22:27:04
