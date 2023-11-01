import re
import requests
from pyzabbix.api import ZabbixAPI
import configparser
import logging
import os
from utils import utilities
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


# Function to obtain the IP - Hostname dictionary
def get_ip_hostname_dict():
    """
    The 'get_ip_hostname_dict' function retrieves a dictionary that maps IP addresses to hostnames for GPS NetRS devices.
    It performs the following tasks:
    1. Reads Zabbix server configuration from 'config.ini'.
    2. Establishes a connection to the Zabbix server using the provided credentials.
    3. Searches for a specific Zabbix template by name ('Template GPS Trimble NetRS').
    4. Retrieves the hosts associated with the found template.
    5. Collects IP addresses of the hosts and verifies their connectivity.
    6. If a host is reachable, adds an entry to the IP - Hostname dictionary.
    7. Closes the Zabbix API session upon completion.

    :param None
    :returns: A dictionary that maps IP addresses to hostnames for GPS NetRS devices.
    :raises: Exception if an error occurs during Zabbix server communication or host connectivity checks.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    zabbix_url = config.get('zabbix', 'zabbix_url')
    zabbix_user = config.get('zabbix', 'zabbix_user')
    zabbix_password = config.get('zabbix', 'zabbix_password')
    try:
        # Configure the connection to your Zabbix server
        zapi = ZabbixAPI(url=zabbix_url, user=zabbix_user, password=zabbix_password)

        # Find the template by name
        template_name = "Template GPS Trimble NetRS"
        template = zapi.template.get(filter={"host": template_name})

        ip_hostname_dict = {}

        if not template:
            logger.error(f"No se encontró el template '{template_name}'")
        else:
            template_id = template[0]["templateid"]
            # Find the hosts associated with the template
            hosts = zapi.host.get(templateids=[template_id], selectInterfaces=["ip", "host"])

            # Collect the IP addresses of the hosts and check their connectivity
            for host in hosts:
                for interface in host["interfaces"]:
                    ip = interface["ip"]
                    is_reachable, response_time = utilities.check_host_connectivity(ip)
                    if is_reachable:
                        hostname = host["host"]
                        ip_hostname_dict[ip] = hostname

        # Close the session
        zapi.user.logout()
        return ip_hostname_dict
    except Exception as e:
        logger.error(f"Error al obtener el diccionario IP - Hostname: {e}")
        return {}


def get_values(ip, arguments):
    """
    The 'get_values' function retrieves specific metrics from a GPS NetRS device by making HTTP requests.
    It takes the IP address of the device and a list of requested arguments as parameters.

    The function performs the following steps:
    1. Constructs the base URL for device-specific data retrieval.
    2. Reads Zabbix server credentials from 'config.ini'.
    3. Iterates through the provided arguments, constructing specific URLs for data retrieval.
    4. Sends HTTP requests with authentication to the device and extracts the response data.
    5. Parses the response text using regular expressions to extract metric values.
    6. Populates a dictionary with metric values, including 'station.code', 'serial.number', 'input.voltage', and 'system.temp'.
    7. Logs any errors that occur during request execution or data processing.
    8. Returns the dictionary of metric values.

    :param ip: The IP address of the GPS NetRS device.
    :type ip: str
    :param arguments: A list of metric arguments to retrieve from the device.
    :type arguments: list
    :returns: A dictionary containing the retrieved metric values.
    :rtype: dict
    :raises: Exception if any errors occur during the HTTP request, data processing, or value retrieval.
    """

    results = {}  # Define 'results' before the 'try' block
    try:
        url_base = f'http://{ip}/prog/Show?'
        config = configparser.ConfigParser()
        config.read('config.ini')
        username = config.get('digitizer_credentials', 'username')
        password = config.get('digitizer_credentials', 'password')
        auth = (username, password)
        results = {}  # Dictionary to store the results

        for argument in arguments:
            full_url = f"{url_base}{argument}"
            try:
                response = requests.get(full_url, auth=auth)
                response.raise_for_status()
                response_text = response.text

                patterns = {
                    # "SystemName": r'name=(\w+)',
                    "SystemName": r'name=([A-Za-z0-9]+)',
                    "SerialNumber": r'sn=(\d+)',
                    "Voltage&input=2": r'volts=([\d.]+)',
                    "Temperature": r'temp=(\d+)'
                }

                for arg, pattern in patterns.items():
                    match = re.search(pattern, response_text)
                    if match:
                        if arg == "SystemName":
                            results["station.code"] = match.group(1)
                        elif arg == "SerialNumber":
                            results["serial.number"] = match.group(1)
                        elif arg == "Voltage&input=2":
                            results["input.voltage"] = match.group(1)
                        elif arg == "Temperature":
                            results["system.temp"] = match.group(1)
            except requests.exceptions.RequestException as e:
                logger.error(f"Error al hacer la solicitud HTTP para {argument}: {e}")
            except Exception as e:
                logger.error(f"Error al procesar el argumento {argument} para {ip}: {e}")
    except Exception as e:
        logger.error(f"Error al obtener valores para {ip}: {e}")
    return results
