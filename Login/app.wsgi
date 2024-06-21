import sys
import os

# Set the path to your virtual environment
venv_path = 'C:/Users/Amritanshu/OneDrive/Desktop/Projects/Login System/env'

# Add the virtual environment's `site-packages` directory to the `sys.path`
sys.path.append(os.path.join(venv_path, 'Lib', 'site-packages'))

# Add the project directory to the `sys.path`
sys.path.append('C:/Users/Amritanshu/OneDrive/Desktop/Projects/Login System')

# Set the `VIRTUAL_ENV` environment variable
os.environ['VIRTUAL_ENV'] = venv_path
os.environ['PATH'] = os.path.join(venv_path, 'Scripts') + os.pathsep + os.environ['PATH']

# Import and run the application
from app import app as application
application.secret_key = 'abcd1234'
