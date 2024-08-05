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
    sudo systemctl start mysql

    # Enable MySQL to start on boot
    sudo systemctl enable mysql

    # Set the MySQl root password and secure the installation
    sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIERD WITH 'mysql_native_password' BY '$MYSQL_ROOTPASSWORD'; FLUSH PRIVILEGES;"
}

