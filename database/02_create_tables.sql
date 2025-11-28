-- BotCommander Table Creation Script
-- Run this after creating the database

USE `bot_commander`;

-- User table
CREATE TABLE IF NOT EXISTS `user` (
    `user_id` INT AUTO_INCREMENT PRIMARY KEY,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `name` VARCHAR(255) NOT NULL,
    `is_admin` BOOLEAN NOT NULL DEFAULT FALSE,
    `created_on` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_email` (`email`),
    INDEX `idx_is_admin` (`is_admin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Login table
CREATE TABLE IF NOT EXISTS `login` (
    `login_id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL,
    `created_on` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `created_by` INT NULL,
    `updated_on` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `updated_by` INT NULL,
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`) ON DELETE CASCADE,
    FOREIGN KEY (`created_by`) REFERENCES `user`(`user_id`) ON DELETE SET NULL,
    FOREIGN KEY (`updated_by`) REFERENCES `user`(`user_id`) ON DELETE SET NULL,
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_is_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- User Bot assignment table
CREATE TABLE IF NOT EXISTS `user_bot` (
    `assign_id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `bot_id` TEXT NOT NULL COMMENT 'Encrypted bot_id',
    `created_on` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `created_by` INT NULL,
    `updated_on` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `updated_by` INT NULL,
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`) ON DELETE CASCADE,
    FOREIGN KEY (`created_by`) REFERENCES `user`(`user_id`) ON DELETE SET NULL,
    FOREIGN KEY (`updated_by`) REFERENCES `user`(`user_id`) ON DELETE SET NULL,
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_is_active` (`is_active`),
    UNIQUE KEY `idx_bot_id` (`bot_id`(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bot Behaviour table
CREATE TABLE IF NOT EXISTS `bots_behaviour` (
    `bot_behav_id` INT AUTO_INCREMENT PRIMARY KEY,
    `assign_id` INT NOT NULL UNIQUE,
    `bot_state` BOOLEAN NOT NULL DEFAULT FALSE,
    `hard_stop_all_trades` BOOLEAN NOT NULL DEFAULT FALSE,
    `listen_to_common_commander` BOOLEAN NOT NULL DEFAULT FALSE,
    `news_based_start_stop` BOOLEAN NOT NULL DEFAULT FALSE,
    `refresh_data_from_bot` BOOLEAN NOT NULL DEFAULT FALSE,
    `created_on` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `created_by` INT NULL,
    `updated_on` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `updated_by` INT NULL,
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (`assign_id`) REFERENCES `user_bot`(`assign_id`) ON DELETE CASCADE,
    FOREIGN KEY (`created_by`) REFERENCES `user`(`user_id`) ON DELETE SET NULL,
    FOREIGN KEY (`updated_by`) REFERENCES `user`(`user_id`) ON DELETE SET NULL,
    INDEX `idx_assign_id` (`assign_id`),
    INDEX `idx_is_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

