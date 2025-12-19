/*
SQLyog Community v12.4.0 (64 bit)
MySQL - 8.0.30 : Database - greengrowth
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`greengrowth` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `greengrowth`;

/*Table structure for table `admin_pemerintah` */

DROP TABLE IF EXISTS `admin_pemerintah`;

CREATE TABLE `admin_pemerintah` (
  `admin_id` int NOT NULL AUTO_INCREMENT,
  `nama_admin` varchar(100) NOT NULL,
  `email_admin` varchar(100) NOT NULL,
  `admin_role` enum('admin') DEFAULT 'admin',
  `password_admin` varchar(25) NOT NULL,
  `foto_admin` varchar(255) DEFAULT NULL,
  `instansi` varchar(150) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`admin_id`),
  UNIQUE KEY `email_admin` (`email_admin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `admin_pemerintah` */

/*Table structure for table `artikel` */

DROP TABLE IF EXISTS `artikel`;

CREATE TABLE `artikel` (
  `artikel_id` int NOT NULL AUTO_INCREMENT,
  `judul_artikel` varchar(150) NOT NULL,
  `deskripsi` text,
  `foto_artikel` varchar(255) DEFAULT NULL,
  `program_id` int NOT NULL,
  `admin_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`artikel_id`),
  KEY `fk_artikel_program` (`program_id`),
  KEY `fk_artikel_admin` (`admin_id`),
  CONSTRAINT `fk_artikel_admin` FOREIGN KEY (`admin_id`) REFERENCES `admin_pemerintah` (`admin_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_artikel_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`program_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `artikel` */

/*Table structure for table `lamaran` */

DROP TABLE IF EXISTS `lamaran`;

CREATE TABLE `lamaran` (
  `lamaran_id` int NOT NULL AUTO_INCREMENT,
  `lowongan_id` int NOT NULL,
  `user_id` int NOT NULL,
  `status_lamaran` enum('menunggu','diterima','ditolak') DEFAULT 'menunggu',
  `applied_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`lamaran_id`),
  KEY `fk_lamaran_lowongan` (`lowongan_id`),
  KEY `fk_lamaran_user` (`user_id`),
  CONSTRAINT `fk_lamaran_lowongan` FOREIGN KEY (`lowongan_id`) REFERENCES `lowongan` (`lowongan_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_lamaran_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `lamaran` */

/*Table structure for table `laporan` */

DROP TABLE IF EXISTS `laporan`;

CREATE TABLE `laporan` (
  `laporan_id` int NOT NULL AUTO_INCREMENT,
  `program_id` int NOT NULL,
  `foto_laporan` varchar(255) DEFAULT NULL,
  `laporan_tanggal` date DEFAULT NULL,
  `laporan_persentase_progres` decimal(5,2) DEFAULT NULL,
  `laporan_output_ekonomi` bigint DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`laporan_id`),
  KEY `fk_laporan_program` (`program_id`),
  CONSTRAINT `fk_laporan_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`program_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `laporan` */

/*Table structure for table `lowongan` */

DROP TABLE IF EXISTS `lowongan`;

CREATE TABLE `lowongan` (
  `lowongan_id` int NOT NULL AUTO_INCREMENT,
  `program_id` int NOT NULL,
  `judul_lowongan` varchar(150) DEFAULT NULL,
  `status_lowongan` enum('dibuka','ditutup') DEFAULT 'dibuka',
  `lowongan_min_umur` int DEFAULT NULL,
  `lowongan_max_umur` int DEFAULT NULL,
  `lowongan_keahlian` text,
  `lowongan_pengalaman` text,
  `lowongan_min_pendidikan` varchar(100) DEFAULT NULL,
  `kuota_pekerja` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`lowongan_id`),
  KEY `fk_lowongan_program` (`program_id`),
  CONSTRAINT `fk_lowongan_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`program_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `lowongan` */

/*Table structure for table `program` */

DROP TABLE IF EXISTS `program`;

CREATE TABLE `program` (
  `program_id` int NOT NULL AUTO_INCREMENT,
  `nama_program` varchar(150) NOT NULL,
  `sektor_program` varchar(100) DEFAULT NULL,
  `tujuan_program` text,
  `lokasi_program` varchar(150) DEFAULT NULL,
  `status_program` enum('perencanaan','berjalan','selesai') DEFAULT 'perencanaan',
  `deskripsi_program` text,
  `admin_id` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`program_id`),
  KEY `fk_program_admin` (`admin_id`),
  CONSTRAINT `fk_program_admin` FOREIGN KEY (`admin_id`) REFERENCES `admin_pemerintah` (`admin_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `program` */

/*Table structure for table `statistik_program` */

DROP TABLE IF EXISTS `statistik_program`;

CREATE TABLE `statistik_program` (
  `statistik_id` int NOT NULL AUTO_INCREMENT,
  `program_id` int NOT NULL,
  `laporan_id` int NOT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`statistik_id`),
  UNIQUE KEY `program_id` (`program_id`),
  KEY `fk_statistik_laporan` (`laporan_id`),
  CONSTRAINT `fk_statistik_laporan` FOREIGN KEY (`laporan_id`) REFERENCES `laporan` (`laporan_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_statistik_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`program_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `statistik_program` */

/*Table structure for table `users` */

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `nama_user` varchar(100) NOT NULL,
  `email_user` varchar(100) NOT NULL,
  `user_role` enum('user') DEFAULT 'user',
  `password_user` varchar(255) NOT NULL,
  `foto_user` varchar(255) DEFAULT NULL,
  `gender` enum('Laki-laki','Perempuan') DEFAULT NULL,
  `tanggal_lahir` date DEFAULT NULL,
  `pendidikan_tertinggi` varchar(100) DEFAULT NULL,
  `softskill` text,
  `hardskill` text,
  `pengalaman` text,
  `no_hp` varchar(20) DEFAULT NULL,
  `alamat` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email_user` (`email_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `users` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
