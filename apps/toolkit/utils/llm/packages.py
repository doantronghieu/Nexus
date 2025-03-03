import sys
import os
from dotenv import load_dotenv
from loguru import logger

def convert_port_to_int(port_value):
    try:
        return int(port_value)
    except (TypeError, ValueError):
        return None

# Store the original os.getenv function
original_getenv = os.getenv

def get_env_port(key, default=None):
    value = original_getenv(key, default)
    if value is not None and key.startswith("PORT_"):
        return convert_port_to_int(value)
    return value

def find_apps_dir_and_load_env():
    current_dir = os.path.abspath('')
    env_files_loaded = []

    while True:
        # Check for and load all .env files in the current directory
        for file in os.listdir(current_dir):
            if file.endswith('.env'):
                env_file = os.path.join(current_dir, file)
                load_dotenv(env_file)
                env_files_loaded.append(env_file)

        # Check if we've reached the 'apps' directory
        if os.path.basename(current_dir) == 'apps':
            break

        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:  # reached root without finding 'apps'
            raise Exception("'apps' directory not found in parent hierarchy")
        current_dir = parent_dir

    return current_dir, env_files_loaded

def setup_paths_and_env():
    apps_dir, env_files = find_apps_dir_and_load_env()
    
    # Add apps directory to sys.path
    if apps_dir not in sys.path:
        sys.path.insert(0, apps_dir)
    
    # Add toolkit to sys.path
    toolkit_path = os.path.join(apps_dir, 'toolkit')
    if os.path.exists(toolkit_path) and toolkit_path not in sys.path:
        sys.path.insert(0, toolkit_path)
    else:
        logger.warning(f"Warning: 'toolkit' directory not found in {apps_dir}")

    return {
        'apps_dir': apps_dir,
        'toolkit_path': toolkit_path,
        'env_files_loaded': env_files
    }

# Run the setup
setup_result = setup_paths_and_env()

# Print out the results
logger.info(f"apps directory: {setup_result['apps_dir']}")
logger.info(f"Toolkit path: {setup_result['toolkit_path']}")
logger.info("Environment files loaded:")
for env_file in setup_result['env_files_loaded']:
    logger.info(f"  - {env_file}")

# Define APP_PATH for compatibility with your original script
APP_PATH = setup_result['apps_dir']
ROOT_PATH = os.path.dirname(APP_PATH)

# Override os.getenv to use our custom get_env_port function
os.getenv = get_env_port
