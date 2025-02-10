Algorithms Used:

1. Quicksort
2. DFS
3. Sequential Search

Structures Used:

1. Trees
2. Multidimensional Arrays
3. Dictionaries

TO RUN THE PROJECT ON LINUX/MACOS DEVICES: 

```bash 
To start the server from the terminal you need to:

touch run_flask_app.sh

nano run_flask_app.sh

Then modify to the nano:

#
#!/bin/bash

# Navigate to the project directory
cd /path/to/your/project/directory || { echo "Directory not found!"; exit 1; }

# Set up and activate the virtual environment
if [ ! -d "myenv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv myenv
fi

# Activate the virtual environment
source myenv/bin/activate

# Ensure Flask and dependencies are installed
pip install flask flask-cors

# Run the Flask app
python3 app.py

#

Then:


chmod +x run_flask_app.sh


And finaly:

./run_flask_app.sh

```bash
