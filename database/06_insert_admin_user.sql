-- Insert admin user: Vishal R (vishal_r)
-- Generated password hash for password: vishal_bot_commander
-- Run this script to create/update the admin user

USE `bot_commander`;

-- Insert user
INSERT INTO `user` (`email`, `name`, `is_admin`, `created_on`)
VALUES ('vishalraykar6@gmail.com', 'Vishal R', TRUE, NOW())
ON DUPLICATE KEY UPDATE 
    `name` = VALUES(`name`),
    `is_admin` = TRUE;

-- Get the user_id
SET @user_id = (SELECT `user_id` FROM `user` WHERE `email` = 'vishal_r' LIMIT 1);

-- Insert login credentials
INSERT INTO `login` (`user_id`, `password`, `created_on`, `created_by`, `is_active`)
VALUES (@user_id, '$2b$12$Q2H37x8iSGOOLQ/IvF.9QedVo8vi3esk8kjM7G69a12MjBCTH3fIm', NOW(), @user_id, TRUE)
ON DUPLICATE KEY UPDATE
    `password` = VALUES(`password`),
    `is_active` = TRUE,
    `updated_on` = NOW(),
    `updated_by` = @user_id;

SELECT CONCAT('Admin user created/updated: ', 'Vishal R', ' (', 'vishal_r', ')') AS result;
