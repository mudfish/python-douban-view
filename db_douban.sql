/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50726
 Source Host           : localhost:3306
 Source Schema         : db_douban

 Target Server Type    : MySQL
 Target Server Version : 50726
 File Encoding         : 65001

 Date: 07/05/2024 15:54:03
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tb_movie
-- ----------------------------
DROP TABLE IF EXISTS `tb_movie`;
CREATE TABLE `tb_movie`  (
  `id` bigint(20) NULL DEFAULT NULL,
  `title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL,
  `year` bigint(20) NULL DEFAULT NULL,
  `directors` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL,
  `casts` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL,
  `rating` double NULL DEFAULT NULL,
  `cover` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL,
  `country` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL,
  `summary` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL,
  `types` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL,
  `lang` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL,
  `release_date` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL,
  `time` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL,
  `url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL
) ENGINE = MyISAM CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
