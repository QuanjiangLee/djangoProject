/*
SQLyog 企业版 - MySQL GUI v8.14 
MySQL - 5.6.24 : Database - safedbstruc
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`safedbstruc` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `safedbstruc`;

/*Table structure for table `adminlogin` */

DROP TABLE IF EXISTS `adminlogin`;

CREATE TABLE `adminlogin` (
  `loginAcc` varchar(50) NOT NULL,
  `LoginTime` datetime NOT NULL,
  PRIMARY KEY (`loginAcc`),
  CONSTRAINT `adminLogin_ibfk_1` FOREIGN KEY (`loginAcc`) REFERENCES `logininf` (`loginAcc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `adminlogin` */

/*Table structure for table `alterhostip` */

DROP TABLE IF EXISTS `alterhostip`;

CREATE TABLE `alterhostip` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `newIp` varchar(40) DEFAULT NULL,
  `oldIp` varchar(40) DEFAULT NULL,
  `alterTime` datetime NOT NULL,
  `newIpExplain` text,
  `oldIpExplain` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `alterhostip` */

/*Table structure for table `alterkeywords` */

DROP TABLE IF EXISTS `alterkeywords`;

CREATE TABLE `alterkeywords` (
  `alterId` int(11) NOT NULL,
  `userId` int(11) NOT NULL,
  `fileHash` char(32) NOT NULL,
  PRIMARY KEY (`alterId`),
  KEY `fileHash` (`fileHash`),
  CONSTRAINT `alterKeywords_ibfk_1` FOREIGN KEY (`fileHash`) REFERENCES `fileinf` (`fileHash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `alterkeywords` */

/*Table structure for table `altermac` */

DROP TABLE IF EXISTS `altermac`;

CREATE TABLE `altermac` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `newMAC` varchar(20) DEFAULT NULL,
  `oldMAC` varchar(20) DEFAULT NULL,
  `alterTime` datetime NOT NULL,
  `newMACExplain` text,
  `oldMACExplain` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `altermac` */

/*Table structure for table `computerinf` */

DROP TABLE IF EXISTS `computerinf`;

CREATE TABLE `computerinf` (
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
  CONSTRAINT `computerInf_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `userinf` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `computerinf` */

/*Table structure for table `dbbackinf` */

DROP TABLE IF EXISTS `dbbackinf`;

CREATE TABLE `dbbackinf` (
  `dbId` int(11) NOT NULL AUTO_INCREMENT,
  `dbName` varchar(255) NOT NULL DEFAULT '自动备份',
  `local_file` varchar(255) DEFAULT NULL,
  `dbTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dbRemark` text,
  `userAcc` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`dbId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `dbbackinf` */

/*Table structure for table `depaertroleinf` */

DROP TABLE IF EXISTS `depaertroleinf`;

CREATE TABLE `depaertroleinf` (
  `deparmentId` int(11) NOT NULL,
  `roleId` int(11) NOT NULL,
  PRIMARY KEY (`deparmentId`,`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `depaertroleinf` */

/*Table structure for table `departmentinf` */

DROP TABLE IF EXISTS `departmentinf`;

CREATE TABLE `departmentinf` (
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

/*Data for the table `departmentinf` */

insert  into `departmentinf`(`departmentId`,`departmentName`,`departmentPeoNum`,`departmentStatus`,`departmentExplian`,`keyPath`,`userLoginStatus`,`province`,`city`,`createTime`,`createUser`,`status`) values (1,'三级部门',0,1,NULL,'null',0,'一级部门','二级部门','2017-04-19 17:05:36','一级部门:二级部门:三级部门:超超管',0),(2,'三级部门',0,1,NULL,'null',0,'陕西省','二级部门','2017-04-19 17:05:57','一级部门:二级部门:三级部门:超超管',0),(3,'三级部门',0,1,NULL,'null',0,'陕西省','公安厅','2017-04-19 17:06:30','一级部门:二级部门:三级部门:超超管',0),(4,'资料处',0,1,NULL,'null',0,'陕西省','公安厅','2017-04-19 17:06:42','一级部门:二级部门:三级部门:超超管',0);

/*Table structure for table `departmentkey` */

DROP TABLE IF EXISTS `departmentkey`;

CREATE TABLE `departmentkey` (
  `keyId` int(11) NOT NULL,
  `departmentId` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`keyId`,`departmentId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `departmentkey` */

/*Table structure for table `fileinf` */

DROP TABLE IF EXISTS `fileinf`;

CREATE TABLE `fileinf` (
  `fileHash` char(32) NOT NULL,
  `fileLocalName` varchar(255) NOT NULL,
  `filePath` varchar(255) NOT NULL,
  `fileSize` int(11) NOT NULL,
  `filePasswd` text,
  PRIMARY KEY (`fileHash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `fileinf` */

/*Table structure for table `filepasswdinf` */

DROP TABLE IF EXISTS `filepasswdinf`;

CREATE TABLE `filepasswdinf` (
  `passwdId` int(11) NOT NULL,
  `passwdPath` varchar(255) NOT NULL,
  `passwdfileName` varchar(255) NOT NULL,
  PRIMARY KEY (`passwdId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `filepasswdinf` */

/*Table structure for table `filepasswdlog` */

DROP TABLE IF EXISTS `filepasswdlog`;

CREATE TABLE `filepasswdlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `alterTime` datetime NOT NULL,
  `passwdId` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `passwdId` (`passwdId`),
  CONSTRAINT `filePasswdLog_ibfk_1` FOREIGN KEY (`passwdId`) REFERENCES `filepasswdinf` (`passwdId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `filepasswdlog` */

/*Table structure for table `fileuploadinf` */

DROP TABLE IF EXISTS `fileuploadinf`;

CREATE TABLE `fileuploadinf` (
  `UploadId` int(11) NOT NULL AUTO_INCREMENT,
  `userId` int(11) NOT NULL,
  `fileHash` char(32) NOT NULL,
  `fileName` varchar(255) NOT NULL,
  `uploadTime` datetime NOT NULL,
  `errId` int(11) DEFAULT NULL,
  PRIMARY KEY (`UploadId`),
  KEY `userId` (`userId`),
  KEY `fileHash` (`fileHash`),
  CONSTRAINT `fileUploadInf_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `userinf` (`userId`),
  CONSTRAINT `fileUploadInf_ibfk_2` FOREIGN KEY (`fileHash`) REFERENCES `fileinf` (`fileHash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `fileuploadinf` */

/*Table structure for table `keywordsinf` */

DROP TABLE IF EXISTS `keywordsinf`;

CREATE TABLE `keywordsinf` (
  `keyId` int(11) NOT NULL AUTO_INCREMENT,
  `keyword` varchar(50) NOT NULL,
  `keyLever` int(11) NOT NULL DEFAULT '0',
  `createUserStatus` int(11) NOT NULL DEFAULT '0',
  `createUserId` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`keyId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `keywordsinf` */

/*Table structure for table `log` */

DROP TABLE IF EXISTS `log`;

CREATE TABLE `log` (
  `logId` int(11) NOT NULL AUTO_INCREMENT,
  `logUpTime` datetime NOT NULL,
  `dataError` varchar(255) DEFAULT NULL,
  `userId` int(11) NOT NULL,
  `logStatus` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`logId`),
  KEY `userId` (`userId`),
  CONSTRAINT `log_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `userinf` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `log` */

/*Table structure for table `logininf` */

DROP TABLE IF EXISTS `logininf`;

CREATE TABLE `logininf` (
  `loginAcc` varchar(50) NOT NULL,
  `loginName` varchar(255) DEFAULT NULL,
  `loginPasswd` varchar(20) NOT NULL DEFAULT '123456',
  `loginStatus` int(11) NOT NULL DEFAULT '1',
  `userId` int(11) NOT NULL,
  `isSuperAdmin` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`loginAcc`),
  KEY `userId` (`userId`),
  CONSTRAINT `loginInf_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `userinf` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `logininf` */

/*Table structure for table `loginlog` */

DROP TABLE IF EXISTS `loginlog`;

CREATE TABLE `loginlog` (
  `Lid` int(11) NOT NULL AUTO_INCREMENT,
  `userId` int(11) NOT NULL,
  `ltime` datetime NOT NULL,
  `lhostIp` varchar(50) DEFAULT NULL,
  `lstatus` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`Lid`),
  KEY `userId` (`userId`)
) ENGINE=MyISAM AUTO_INCREMENT=37250 DEFAULT CHARSET=utf8;

/*Data for the table `loginlog` */

/*Table structure for table `noticedata` */

DROP TABLE IF EXISTS `noticedata`;

CREATE TABLE `noticedata` (
  `Nid` int(11) NOT NULL AUTO_INCREMENT,
  `Ntime` datetime NOT NULL DEFAULT '1990-01-01 00:00:00',
  `Ntitle` varchar(255) NOT NULL DEFAULT 'null',
  `Nbody` text NOT NULL,
  `Nstatus` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`Nid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `noticedata` */

/*Table structure for table `portinf` */

DROP TABLE IF EXISTS `portinf`;

CREATE TABLE `portinf` (
  `port` int(11) NOT NULL,
  `PortExplan` text,
  PRIMARY KEY (`port`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `portinf` */

/*Table structure for table `powerinf` */

DROP TABLE IF EXISTS `powerinf`;

CREATE TABLE `powerinf` (
  `powerId` int(11) NOT NULL AUTO_INCREMENT,
  `powerName` varchar(255) NOT NULL,
  `powerExplan` text NOT NULL,
  `PowerStatus` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`powerId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `powerinf` */

/*Table structure for table `remoterecord` */

DROP TABLE IF EXISTS `remoterecord`;

CREATE TABLE `remoterecord` (
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

/*Data for the table `remoterecord` */

/*Table structure for table `roleinf` */

DROP TABLE IF EXISTS `roleinf`;

CREATE TABLE `roleinf` (
  `roleId` int(11) NOT NULL AUTO_INCREMENT,
  `roleName` varchar(255) NOT NULL,
  `rolePNum` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `roleinf` */

/*Table structure for table `rolepower` */

DROP TABLE IF EXISTS `rolepower`;

CREATE TABLE `rolepower` (
  `roleId` int(11) NOT NULL,
  `powerId` int(11) NOT NULL,
  PRIMARY KEY (`roleId`,`powerId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `rolepower` */

/*Table structure for table `selectcode` */

DROP TABLE IF EXISTS `selectcode`;

CREATE TABLE `selectcode` (
  `selectId` int(11) NOT NULL AUTO_INCREMENT,
  `selectTitle` varchar(255) NOT NULL,
  `selectBody` text,
  `selectStatus` int(11) NOT NULL DEFAULT '1',
  `selectExplain` text,
  PRIMARY KEY (`selectId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `selectcode` */

/*Table structure for table `selfcheck` */

DROP TABLE IF EXISTS `selfcheck`;

CREATE TABLE `selfcheck` (
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
  CONSTRAINT `tem_userscan` FOREIGN KEY (`userId`) REFERENCES `userinf` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `selfcheck` */

/*Table structure for table `usererrinf` */

DROP TABLE IF EXISTS `usererrinf`;

CREATE TABLE `usererrinf` (
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
  PRIMARY KEY (`errId`),
  KEY `fileHash` (`fileHash`),
  KEY `userId` (`userId`),
  KEY `errTime` (`errTime`),
  CONSTRAINT `userErrInf_ibfk_2` FOREIGN KEY (`userId`) REFERENCES `userinf` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `usererrinf` */

/*Table structure for table `userinf` */

DROP TABLE IF EXISTS `userinf`;

CREATE TABLE `userinf` (
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

/*Data for the table `userinf` */

insert  into `userinf`(`userId`,`userNo`,`userName`,`userSex`,`userTel`,`userPosition`,`userStatus`,`registStatus`,`loginStatus`,`userIdentify`,`departmentId`,`userLever`,`userPasswd`,`userPositionStatus`) values (1,'2017141','超高管','null','null','超高管',1,0,0,'null',1,'null','*6A7A490FB9DC8C33C2B025A91737077A7E9CC5E5',2),(2,'2017142','超管','null','null','超管',1,0,0,'null',2,'null','*6A7A490FB9DC8C33C2B025A91737077A7E9CC5E5',2),(3,'2017143','普管','null','null','普管',1,0,0,'null',3,'null','*6A7A490FB9DC8C33C2B025A91737077A7E9CC5E5',1),(4,'2017144','一般人','null','null','一般人',1,0,0,'null',4,'null','*6A7A490FB9DC8C33C2B025A91737077A7E9CC5E5',0);

/*Table structure for table `userpowerinf` */

DROP TABLE IF EXISTS `userpowerinf`;

CREATE TABLE `userpowerinf` (
  `userId` int(11) NOT NULL,
  `powerId` int(11) NOT NULL,
  PRIMARY KEY (`userId`,`powerId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `userpowerinf` */

/*Table structure for table `userroleinf` */

DROP TABLE IF EXISTS `userroleinf`;

CREATE TABLE `userroleinf` (
  `userId` int(11) NOT NULL,
  `roleId` int(11) NOT NULL,
  PRIMARY KEY (`userId`,`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `userroleinf` */

/*Table structure for table `userscan` */

DROP TABLE IF EXISTS `userscan`;

CREATE TABLE `userscan` (
  `usId` int(11) NOT NULL AUTO_INCREMENT,
  `fileName` varchar(255) DEFAULT NULL,
  `filePath` varchar(255) DEFAULT NULL,
  `keywords` varchar(255) DEFAULT NULL,
  `scanTime` datetime DEFAULT NULL,
  `userNo` varchar(50) DEFAULT NULL,
  `userId` int(11) DEFAULT NULL,
  `keyExtend` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`usId`)
) ENGINE=MyISAM AUTO_INCREMENT=15182 DEFAULT CHARSET=utf8;

/*Data for the table `userscan` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
