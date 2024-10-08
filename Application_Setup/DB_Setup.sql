-- DATABASE CREATION
DROP DATABASE IF EXISTS csd_database;

CREATE DATABASE csd_database;

-- USER CREATION
DROP USER IF EXISTS 'csd_user'@'%';

CREATE USER 'csd_user'@'%' IDENTIFIED BY 'Csd_password@123';

GRANT ALL PRIVILEGES ON *.* TO 'csd_user'@'%' WITH GRANT OPTION;

FLUSH PRIVILEGES;