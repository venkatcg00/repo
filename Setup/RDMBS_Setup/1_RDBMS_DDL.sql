SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS = 0;

CREATE TABLE IF NOT EXISTS CSD_SOURCES(
    SOURCE_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    SOURCE_NAME VARCHAR(255) NOT NULL,
    SOURCE_FILE_TYPE VARCHAR(255) NOT NULL,
    HOST_NAME VARCHAR(255),
    PORT VARCHAR(255),
    DATABASE_NAME VARCHAR(255),
    USER_NAME VARCHAR(255),
    PASSWORD VARCHAR(255),
    FILE_PATH VARCHAR(255),
    API_ENDPOINT VARCHAR(255),
    SECURITY_PROTOCOL VARCHAR(255),
    AUTH_METHOD VARCHAR(255),
    CONNECTION_PARAMETERS VARCHAR(255),
    SOURCE_TYPE VARCHAR(255) NOT NULL,
    LAST_LOADED_RECORD_ID VARCHAR(255),
    DESCRIPTION VARCHAR(255),
    ACTIVE_FLAG CHAR(1) NOT NULL,
    START_DATE DATETIME NOT NULL,
    END_DATE DATETIME NOT NULL
);

ALTER TABLE
    CSD_SOURCES ADD UNIQUE csd_sources_source_name_unique(SOURCE_NAME);

ALTER TABLE
    CSD_SOURCES ADD INDEX csd_sources_file_path_index(FILE_PATH);



CREATE TABLE IF NOT EXISTS CSD_TRANSFORMATIONS(
    TRANSFORMATION_ID INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    SOURCE_ID INT NOT NULL,
    SOURCE_COLUMN_NAME VARCHAR(255) NOT NULL,
    TARGET_COLUMN_NAME VARCHAR(255) NOT NULL,
    TARGET_TABLE_NAME VARCHAR(255) NOT NULL,
    TARGET_SOURCE_ID INT NOT NULL,
    TRANSFORMATION_RULE VARCHAR(255) NOT NULL,
    ACTIVE_FLAG CHAR(1),
    START_DATE DATETIME NOT NULL,
    END_DATE DATETIME NOT NULL
);

ALTER TABLE
    CSD_TRANSFORMATIONS ADD INDEX CSD_TRANSFORMATIONS_source_id_index(SOURCE_ID);

ALTER TABLE
    CSD_TRANSFORMATIONS ADD INDEX CSD_TRANSFORMATIONS_transformation_rule_index(TRANSFORMATION_RULE);



CREATE TABLE IF NOT EXISTS CSD_DM(
    CSD_ID INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    SOURCE_ID INT NOT NULL,
    SOURCE_SYSTEM_IDENTIFIER VARCHAR(255) NOT NULL,
    AGENT_ID INT NOT NULL,
    INTERACTION_DATE DATETIME,
    CUSTOMER_TYPE VARCHAR(255),
    SUPPORT_AREA VARCHAR(255),
    HANDLE_TIME INT,
    WORK_TIME INT,
    FIRST_CONTACT_RESOLUTION CHAR(255),
    CUSTOMER_RATING INT,
    RESOLUTION_CATEGORY VARCHAR(255),
    QUERY_STATUS VARCHAR(255),
    IS_VALID_DATA VARCHAR(255),
    ACTIVE_FLAG CHAR(1) NOT NULL,
    START_DATE DATETIME NOT NULL,
    END_DATE DATETIME NOT NULL
);

ALTER TABLE
    CSD_DM ADD UNIQUE csd_dm_source_system_identifier_unique(SOURCE_SYSTEM_IDENTIFIER);

ALTER TABLE
    CSD_DM ADD INDEX csd_dm_source_id_index(SOURCE_ID);

ALTER TABLE
    CSD_DM ADD INDEX csd_dm_agent_id_index(AGENT_ID);

ALTER TABLE
    CSD_DM ADD INDEX csd_dm_active_flag_index(ACTIVE_FLAG);



CREATE TABLE CSD_AGENTS(
    AGENT_ID INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    FIRST_NAME VARCHAR(255) NOT NULL,
    MIDDLE_NAME VARCHAR(255) NOT NULL,
    LAST_NAME VARCHAR(255) NOT NULL,
    PSUEDO_NAME VARCHAR(255) NOT NULL,
    SUPPORT_TEAM VARCHAR(255) NOT NULL,
    ACTIVE_FLAG CHAR(1),
    START_DATE DATETIME NOT NULL,
    END_DATE DATETIME NOT NULL
);


ALTER TABLE
    CSD_DM ADD CONSTRAINT csd_dm_agent_id_foreign FOREIGN KEY(AGENT_ID) REFERENCES CSD_AGENTS(AGENT_ID);

ALTER TABLE
    CSD_DM ADD CONSTRAINT csd_dm_source_id_foreign FOREIGN KEY(SOURCE_ID) REFERENCES CSD_SOURCES(SOURCE_ID);

ALTER TABLE
    CSD_TRANSFORMATIONS ADD CONSTRAINT CSD_TRANSFORMATIONS_source_id_foreign FOREIGN KEY(SOURCE_ID) REFERENCES CSD_SOURCES(SOURCE_ID);
    
ALTER TABLE
    CSD_TRANSFORMATIONS ADD CONSTRAINT CSD_TRANSFORMATIONS_target_source_id_foreign FOREIGN KEY(TARGET_SOURCE_ID) REFERENCES CSD_SOURCES(SOURCE_ID);

ALTER TABLE
    CSD_AGENTS ADD CONSTRAINT csd_agnets_source_name_foerign FOREIGN KEY(SUPPORT_TEAM) REFERENCES CSD_SOURCES(SOURCE_NAME);