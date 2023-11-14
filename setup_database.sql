CREATE DATABASE IF NOT EXISTS profile_db;
USE profile_db;
CREATE USER IF NOT EXISTS 'kingsley_profile_db'@'localhost';
SET PASSWORD FOR 'kingsley_profile_db'@'localhost' = 'kingsley_super_user';
GRANT ALL PRIVILEGES on profile_db.* TO 'kingsley_profile_db'@'localhost';
GRANT SELECT ON performance_schema.* TO 'kingsley_profile_db'@'localhost';