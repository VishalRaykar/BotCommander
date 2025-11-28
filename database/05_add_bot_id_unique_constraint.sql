-- Migration script to add UNIQUE constraint to bot_id in user_bot table
-- Run this if you have an existing database without the unique constraint on bot_id

USE `bot_commander`;

-- Check for duplicate bot_ids before adding unique constraint
-- This will help identify any existing duplicates
SELECT `bot_id`, COUNT(*) as count
FROM `user_bot`
WHERE `is_active` = TRUE
GROUP BY `bot_id`
HAVING count > 1;

-- If duplicates exist, you need to resolve them first
-- Then add the unique constraint

-- Check if index exists before adding (MySQL 5.7+ compatible)
SET @dbname = DATABASE();
SET @tablename = 'user_bot';
SET @indexname = 'idx_bot_id';

SET @idx_exists = (
    SELECT COUNT(*) 
    FROM INFORMATION_SCHEMA.STATISTICS 
    WHERE TABLE_SCHEMA = @dbname 
    AND TABLE_NAME = @tablename 
    AND INDEX_NAME = @indexname
);

SET @sql = IF(@idx_exists = 0,
    CONCAT('ALTER TABLE `', @tablename, '` ADD UNIQUE INDEX `', @indexname, '` (`bot_id`(255))'),
    'SELECT "Index idx_bot_id already exists" AS message'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

