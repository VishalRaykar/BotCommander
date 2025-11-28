-- Migration script to add is_admin column to existing user table
-- Run this if you have an existing database without the is_admin column
-- Compatible with MySQL 5.7+

USE `bot_commander`;

-- Add is_admin column (will fail gracefully if column already exists)
-- For MySQL 8.0+, you can use: ADD COLUMN IF NOT EXISTS
-- For MySQL 5.7, run this script and ignore the error if column exists

-- Check and add column (MySQL 8.0+ syntax)
-- ALTER TABLE `user` ADD COLUMN IF NOT EXISTS `is_admin` BOOLEAN NOT NULL DEFAULT FALSE AFTER `name`;

-- For MySQL 5.7 compatibility, use this approach:
SET @col_exists = (
    SELECT COUNT(*) 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = 'bot_commander' 
    AND TABLE_NAME = 'user' 
    AND COLUMN_NAME = 'is_admin'
);

SET @sql = IF(@col_exists = 0,
    'ALTER TABLE `user` ADD COLUMN `is_admin` BOOLEAN NOT NULL DEFAULT FALSE AFTER `name`',
    'SELECT "Column is_admin already exists" AS message'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Add index if it doesn't exist
SET @idx_exists = (
    SELECT COUNT(*) 
    FROM INFORMATION_SCHEMA.STATISTICS 
    WHERE TABLE_SCHEMA = 'bot_commander' 
    AND TABLE_NAME = 'user' 
    AND INDEX_NAME = 'idx_is_admin'
);

SET @sql = IF(@idx_exists = 0,
    'ALTER TABLE `user` ADD INDEX `idx_is_admin` (`is_admin`)',
    'SELECT "Index idx_is_admin already exists" AS message'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Set first user (user_id = 1) as admin if exists
UPDATE `user` 
SET `is_admin` = TRUE 
WHERE `user_id` = 1 AND (`is_admin` = FALSE OR `is_admin` IS NULL);
