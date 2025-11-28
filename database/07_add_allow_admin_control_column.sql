-- 07_add_allow_admin_control_column.sql
-- Adds allow_admin_control column to user_bots table for admin control toggle

ALTER TABLE user_bots
ADD COLUMN allow_admin_control BOOLEAN NOT NULL DEFAULT FALSE AFTER is_active;