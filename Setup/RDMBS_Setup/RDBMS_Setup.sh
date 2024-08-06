#!/bin/bash

# Define the configuration file.
CONFIG_FILE="RDBMS_Parameters.cfg"

# Check if the configuration file exists.
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Configuration file $CONFIG_FILE not found!"
    exit 1
fi

# Secure the configuration file by setting the permissions to 600
echo "Securing configuration file..."
chmod 600 $CONFIG_FILE

# Source the configuration file to read parameters
source $CONFIG_FILE

# Check for required parameters.
if [ -z "$DB_USER" ] || [ -z "$DB_PASS" ] || [ -z "$DB_NAME" ]; then
    echo "Configuration file does not contain required parameters."
    exit 1
fi

# Function to install MySQL Server
install_mysql() {
    echo "Installing MySQL Server..."

    # Update package information.
    sudo apt-get update

    # Install MySQL server
    sudo apt-get install -y mysql-server

    # Start MySQL server
    sudo service mysql start
}

# Function to create MySQL database and user
create_db_user_and_database() {
    echo "Creating MySQL user and database..."

    # Execute SQL commands to create user and database
    mysql -u root <<EOF
    CREATE DATABASE IF NOT EXISTS $DB_NAME;

    CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';

    GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';
    FLUSH PRIVILEGES;
EOF
    echo "Created DB user and DB successfully."
}

# Function to execute DDL and DML SQL files
execute_sql_files() {
    echo "Executing SQL files..."

    # Loop through each .sql file and execute it
    for sql_file in $(ls *.sql); do
        if [ -f "$sql_file" ]; then
            echo "Executing "$sql_file""
            mysql -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" < "$sql_file"
        fi
    done 
}

# Main script execution
install_mysql
create_db_user_and_database
execute_sql_files

echo "MySQL installation is complete."

exit 0