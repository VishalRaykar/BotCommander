-- 08_add_validity_column.sql
-- Adds validity column to user_bot table for bot assignment expiry

ALTER TABLE user_bot
ADD COLUMN validity DATETIME NULL AFTER allow_admin_control;