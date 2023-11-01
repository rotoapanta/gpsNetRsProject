import subprocess
import logging
import os
import datetime

# Get the current date in the desired format (Year-Month-Day)
current_date = datetime.date.today().strftime("%Y-%m-%d")
# Get the full path to the '_gps_netrs.log' file in the 'logs' folder
logs_folder = 'logs'
if not os.path.exists(logs_folder):
    os.makedirs(logs_folder)

# File name of the log file with the date
log_file = os.path.join(logs_folder, f'{current_date}_gps_netrs.log')
# Configure the error logging system
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %('
                                                                   'message)s')
logger = logging.getLogger(__name__)


def check_host_connectivity(ip):
    """
    The 'check_host_connectivity' function checks the connectivity to a specified IP address using the 'ping' command.

    This function performs the following steps:
    1. Executes a 'ping' command to the provided IP address with a single ICMP packet.
    2. Analyzes the return code of the 'ping' command to determine if the host is reachable.
    3. Logs the result and returns a tuple indicating connectivity status and the response or error message.

    :param ip: The IP address to check for connectivity.
    :type ip: str
    :return: A tuple with two elements:
        - A boolean indicating connectivity status (True if reachable, False otherwise).
        - A string with the response message if the host is reachable, or an error message if the host is not reachable.
    :raises: subprocess.CalledProcessError (if the 'ping' command execution fails)
    """

    try:
        result = subprocess.run(["ping", "-c", "1", ip], capture_output=True, text=True, check=True)
        if result.returncode == 0:
            logger.info(f"Conexión exitosa a {ip}")
            return True, result.stdout
        else:
            logger.error(f"Fallo en la conexión a {ip}: {result.stderr}")
            return False, result.stderr
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al ejecutar el comando 'ping': {e}")
        return False, str(e)
