#!/bin/bash

# This script is used to setup the enivornment for the project in a Ubuntu based system.

# Function to convert relative paths into absolute paths
create_parameters() {
    local repo_name="$1"
    local text_file="$2"

    # Check if the text file exists
    if [[ ! -f "$text_file" ]]; then
        echo "Text file not found!"
        return 1
    fi

    # Get the absolute path of the repository
    current_directory="$(pwd)"
    extracted_path="${current_directory%%$repo_name*}$repo_name/"

    # Create an output file for the absolute paths
    local output_file="Setup_parameters.txt" 
    > "$output_file"

    # Read the text file line by line
    while IFS='=' read -r key relative_path; do
        # Check if key and relative_path are not empty
        if [[ -n "$key" && -n "$relative_path" ]]; then
            # Trim possible spaces around key and relative_path
            key=$(echo "$key" | xargs)
            relative_path=$(echo "$relative_path" | xargs)

            # Create the absolute path
            local absolute_path="$extracted_path$relative_path"
            # Write te key and absolute path to the output file
            echo "$key=$absolute_path" >> "$output_file"
        else
            echo "Warning: Skipping malformed line: $key=$relative_path"
        fi
    done < "$text_file"
    echo "DB_USER=csd_user" >> "$output_file"
    echo "DB_NAME=csd_database" >> "$output_file"
    echo "DB_PASSWORD=Csd_password@123" >> "$output_file"
    echo "DB_HOST=127.0.0.1" >> "$output_file"

    echo "Parameter file has created with name $output_file"
}


# Function to check if Python has been installed.
install_python() {
    if command -v python3 > /dev/null 2>&1; then
        echo "Python is already installed."
    else
        echo "Python is not installed. Installing Python."
        sudo apt-get update > /dev/null 2>&1
        sudo apt-get install -y python3 > /dev/null 2>&1
        echo "Python has been installed."
    fi
}


# Function to check and install missing python libraries
install_libraries() {
    REQUIREMENTS_FILE="pip_requirements.txt"
    if [ ! -f "$REQUIREMENTS_FILE" ]; then
        echo "Requriements file '$REQUIREMENTS_FILE' is not found."
        exit 1
    fi

    while IFS= read -r library; do
        if ! python3 -c "import $library" > /dev/null 2>&1; then
            echo "Installing $library..."
            pip install $library > /dev/null 2>&1
        else
            echo "$library is already installed."
        fi
    done < "$REQUIREMENTS_FILE"
}


# Function to check and create direcotries and files
check_and_create_file() {
    local file_path="$1"

    # Check if the input is an absolute path
    if [[ "$file_path" != /* ]]; then
        echo "Error: Please provide an absolute path."
        return 1
    fi

    # Extract the directory path from the file path.
    local dir_path=$(dirname "$file_path")

    # Create all missing directories
    mkdir -p "$dir_path"

    if [ $? -ne 0 ]; then
        echo "Error: could not create directories leadin to '$file_path'"
        return 1
    fi

    # Check if file exists and is accesible
    if [ -f "$file_path" ]; then
        echo "File '$file_path' already exists."
    else
        echo "File '$file_path' does not exist. Creating the file..."
        touch "$file_path"
        chmod 7777 "$file_path"

        if [ $? -eq 0 ]; then
            echo "File '$file_path' created successfully."
        else
            echo "Error: Could not create file '$file_path'."
        fi
    fi
}


# Function to check if MySQL is installed.
check_mysql_installation() {
    if command -v mysql > /dev/null 2>&1 ; then
        echo "MySQL is installed."
        return 0
    else
        echo "MySQL is not installed. Installing MySQL..."
        apt-get install -y mysql-server > /dev/null 2>&1

        if [ $? -ne 0 ]; then
            echo "Error: Failed to install MySQL."
            exit 1
        fi
        
        echo "MySQL installed successfully."
        return 0
    fi
}


# Function to check if MySQL is running
check_mysql_running() {
    # Check if the MySQL process is running
    if service mysql status | grep -q "stopped"; then
        echo "MySQL is not running, Starting MySQL..."
        service mysql start

        # Check if MySQL startd successfully
        if service mysql status | grep -q "running"; then
            echo "MySQL has started successfully."
        else
            echo "Error: Failed to start MySQL."
        fi
    else
        echo "MySQL is running"
    fi
}


# Function to execute sql scripts
execute_sql_scripts () {
    local sql_script="$1"

    # Check if the SQL script exists
    if [[ -f "$sql_script" ]]; then
        echo "Executing script: $sql_script."

        # Execute the SQL script using MySQL client.
        mysql -u root < "$sql_script"

        if [[ $? -eq 0 ]]; then
            echo "SQL script executed successfully!"
        else
            echo "Error occured while executing the SQL script."
        fi
    else
        echo "File not found: $sql_script."
        return 1
    fi
}


# Function to run scripts in parallel
run_scripts_in_parallel() {
    local pids=()       # Array to store the process IDs
    local scripts=()    # Array to store the script names in execution
    local logs=()       # Array to store the log file names in execution

    # Iterate over all variables deifined in the config file
    for var in $(compgen -A variable | grep "PARALLEL_SCRIPT_"); do
        script="${!var}"
        if [[ -f "$script" ]]; then
            # Run the script in the background, redirect output to a log file, and store its PID
            python3 "$script" >"${var}.log" 2>&1 & pids+=($!)      # Append the PID of the script to the array
            scripts+=("$script") 
            logs+=("${var}.log")                                  # Append the script name to the array
            echo "Started $script with PID ${pids[-1]}."
        else
            echo "Script $script not found."
        fi  
    done

    # Display the menu
    while [[ "${#scripts[@]}" -ne 0 ]]; do
        echo "The scripts running are listed below. Select a script to kill:"
        for i in "${!scripts[@]}"; do
            echo "$((i + 1))) ${scripts[i]}"
        done
        scripts_count=${#scripts[@]}
        increment=1
        total_count=$(($scripts_count + $increment))
        if [[ "${#scripts[@]}" -ne 0 ]]; then
            echo "$total_count) all"
        fi

        read -r choice

        # Check if the input is valid
        if [[ "$choice" -ge 1 && "$choice" -le "${#scripts[@]}" ]]; then
            # Kill the selected script
            index=$((choice - 1))
            kill "${pids[$index]}" 2>/dev/null
            rm "${logs[$index]}"
            echo "Terminated ${scripts[$index]} with PID ${pids[$index]}}"
            unset pids[$index] scripts[$index] logs[$index]
            pids=("${pids[@]}") scripts=(${scripts[@]})     # Re-index arrays
        elif [[ "$choice" -eq "$total_count" ]]; then
            # Kill all scripts
            echo "Terminating all scripts..."
            for pid in "${pids[@]}"; do
                kill "$pid" 2>/dev/null
            done

            # Delete all log files
            for log in "${logs[@]}"; do
                rm "$log"
            done
            break
        else
            echo "Invalid selection. Please try again."
        fi
    done
}


# Main Script starts here
apt-get -y update > /dev/null 2>&1
apt-get -y upgrade > /dev/null 2>&1

echo "Executing parameters creating function"
create_parameters "$1" "File_folder_paths.txt"

# Source parameter file
source "Setup_parameters.txt"

echo "Executing Python installation function"
install_python
echo "Completed executing Python installation function"

echo "Executing function to install Python libraries"
install_libraries
echo "Completed executing function to install Python libraries"

# Check and create the directories as defined in the config file.
check_and_create_file "$CSV_FILE"
check_and_create_file "$JSON_FILE"
check_and_create_file "$XML_FILE"

echo "Checking for MySQL insallation."
check_mysql_installation
check_mysql_running
execute_sql_scripts "$DB_SETUP_SCRIPT"
execute_sql_scripts "$DDL_SCRIPT"
execute_sql_scripts "$DML_SCRIPT"
echo "Pre checks are complete."

# Parallel execution
run_scripts_in_parallel

echo "All scripts have been terminated."