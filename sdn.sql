-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema sdn
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema sdn
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `sdn` DEFAULT CHARACTER SET latin1 ;
USE `sdn` ;

-- -----------------------------------------------------
-- Table `sdn`.`link_energy`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sdn`.`link_energy` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `switch_src` VARCHAR(45) NULL DEFAULT NULL,
  `switch_dst` VARCHAR(45) NULL DEFAULT NULL,
  `time` INT(11) NULL DEFAULT NULL,
  `wh` FLOAT NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 1521
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `sdn`.`stats`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sdn`.`stats` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `switch` VARCHAR(45) NOT NULL,
  `tx_bytes` INT(100) NULL DEFAULT NULL,
  `rx_bytes` INT(100) NULL DEFAULT NULL,
  `port_no` INT(10) NULL DEFAULT NULL,
  `time` INT(10) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 10005
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `sdn`.`switch_energy`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sdn`.`switch_energy` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `switch` VARCHAR(45) NULL DEFAULT NULL,
  `time` INT(11) NULL DEFAULT NULL,
  `wh` FLOAT NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 381
DEFAULT CHARACTER SET = latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
