#!/bin/bash

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if main.py exists
if [ ! -f "$DIR/main.py" ]; then
    echo "Error: main.py not found in directory $DIR"
    exit 1
fi

# Create the ssh_monitor script
echo "#!/bin/bash" > ssh_monitor
echo "python3 \"$DIR/main.py\"" >> ssh_monitor

# Check if creating ssh_monitor was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to create ssh_monitor script"
    exit 1
fi

# Set execute permissions for ssh_monitor
sudo chmod +x ssh_monitor

# Check if setting execute permissions was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to set execute permissions for ssh_monitor"
    exit 1
fi

# Copy ssh_monitor to /bin/ to make it globally accessible
sudo cp ssh_monitor /bin/

# Check if copying to /bin/ was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to copy ssh_monitor to /bin/"
    exit 1
fi

echo "ssh_monitor script has been successfully created and copied to /bin/"
