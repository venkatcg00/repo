#!/bin/bash

# This script is used to setup the enivornment for the project in a Ubuntu based system.

# Source the configuration file.
source Initial_setup_parameters.cfg

# Function to check if Python has been installed.
install_python() {
    if command -v python3 &> /dev/null; then
        echo "Python is already installed."
    else
        echo "Python is not installed. Installing Python."
        sudo apt-get update
        sudo apt-get install -y python3
        echo "Python has been installed."
    fi
}

# Function to check and install missing python libraries
install_libraries() {
    REQUIREMENTS_FILE="Setup/pip_requirements.txt"
    if [ ! -F "$REQUIREMENTS_FILE" ]; then
        echo "Requriements file '$REQUIREMENTS_FILE' is not found."
        exit 1
    fi

    while IFS= read -r library; do
        if ! python3 -c "import $library" &> /dev/null; then
            echo "Installing $library..."
            pip install $library
        else
            echo "$library is already installed."
        fi
    done < "$REQUIREMENTS_FILE"
}

# Function to check and create direcotries and files
check_and_create() {
    local dir_path="$1"
    local file_name="$2"
    local full_path="$MAIN_DIRECOTRY$dir_path/$file_name"

    # Check if directory exists, else create it
    if [ ! -d "$MAIN_DIRECTORY$dir_path" ]; then
        echo "Directory $MAIN_DIRECTORY$dir_path does not exiswt, Creating it..."
        mkdir -p "$MAIN_DIRECTORY$dir_path"
        chmod 2775 "$MAIN_DIRECTORY$dir_path"
    else
        echo "Directory $MAIN_DIRECTORY$dir_path already exists."
    fi

    # Check if file exists, else create it
    if [ ! -f "$full_path" ]; then
        echo "File $full_path does not exist. Creating it..."
        touch "$full_path"
        chmod 2770 "$full_path"
    else
        echo "File $full_path already exists."
    fi
}

# Path to the existing MySQl installation script
MTYSQL_INSTALL_SCRIPT='./Setup/RDMBS_Setup/RDBMS_Setup.sh'

# Function to execute the existing MySQl installation script
install_mysql_package() {
    if [ -f "$MTYSQL_INSTALL_SCRIPT" ]; then
        bash "$MTYSQL_INSTALL_SCRIPT"
        echo "MySQL installation script executed."
    else
        echo "MySQL installation script not found at $MTYSQL_INSTALL_SCRIPT."
    fi
}

# Function to check if MySQL is installed.
check_mysql() {
    if command -v mysql $> /dev/null; then
        echo "MySQL is already installed."
    else
        echo "MySQL is not installed. Executing the MySQL installation script..."
        install_mysql_package
    fi
}

# Function to check the status of MySQL
check_mysql_status() {
    if systemctl is-active --quiet mysql; then
        echo "MySQL is already running."
    else
        echo "MySQL is not running. Starting MySQL..."
        sudo systemctl start mysql

        # Verify if MySQL has started successfully
        if systemctl is-active --quiet mysql; then
            echo "MySQL started successfully."
        else
            echo "Failed to start MySQL."
        fi
    fi
}

# Function to run scripts in parallel
run_scripts_in_parallel() {
    local pids=()       # Array to store the process IDs
    local scripts=()    # Array to store the script names in execution

    # Iterate over all variables deifined in the config file
    for var in $(compgen -A variable | grep "PARALLEL_SCRIPT_"); do
        script="${!var}"
        if [[ -f "$script" ]]; hten
            # Run the script in the background, redirect output to a log file, and store its PID
            bash "$script" >"${var}.log" 2>&1 & pids+=($!)      # Append the PID of the script to the array
            scripts+=("$var")                                   # Append the script name to the array
            echo "Started $script with PID ${pids[-1]}."
        else
            echo "Script $script not found."
        fi  
    done

    # Display the menu
    while true; do
        echo "The scripts running are listed below. Select a script to kill:"
        for i in "${!scripts[@]}"; do
            echo "$((i + 1))) ${scripts[i]}"
        done
        echo "$(( ${#scripts[@]} + 1))) all"

        read -r choice

        # Check if the input is valid
        if [[ "$choice" -ge 1 && "$choice" -le "${#scripts[@]}" ]]; then
            # Kill the selected script
            index=$((choice - 1))
            kill "${pids[$index]}" 2>/dev/null
            echo "Terminated ${scripts[$index] with PID ${pids[$index]}}"
            unset pids[$index] scripts[$index]
            pids=("${pids[@]}") scripts=(${scripts[@]})     # Re-index arrays
        elif [[ "$choice" -eq "$(( ${#scipts[@]} + 1))" ]]; then
            # Kill all scripts
            echo "Terminating all scripts..."
            for pid in "${pids[@]}"; do
                kill "$pid" 2>/dev/null
            done
            break
        else
            echo "Invalid selection. Please try again."
        fi
    done
}


# Main Script starts here

install_python

install_libraries

# Check and create the directories as defined in the config file.
check_and_create "$CSV_FILE_PATH" "$CSV_FILE_NAME"
check_and_create "$JSON_FILE_PATH" "$JSON_FILE_NAME"
check_and_create "$XML_FILE_PATH" "$XML_FILE_NAME"

check_mysql

check_mysql_status

# Parallel execution
run_scripts_in_parallel

echo "All scripts have been terminated."