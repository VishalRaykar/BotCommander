-- Migration script to add bots_behaviour table
-- Run this if you have an existing database without the bots_behaviour table

USE `bot_commander`;

-- Create bots_behaviour table
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

-- Create default behaviour records for existing bot assignments
-- Only insert records that don't already exist
INSERT IGNORE INTO `bots_behaviour` (`assign_id`, `created_on`)
SELECT `assign_id`, NOW()
FROM `user_bot`
WHERE `is_active` = TRUE;

