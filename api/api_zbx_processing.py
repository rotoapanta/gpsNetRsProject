import re
import requests
from pyzabbix.api import ZabbixAPI
from ping3 import ping
import configparser
import logging
import os

# Configura el registro de errores en un archivo llamado 'error.log' en la carpeta 'logs'
logs_folder = 'logs'
if not os.path.exists(logs_folder):
    os.makedirs(logs_folder)

#log_file = os.path.join(logs_folder, 'error.log')
log_file = '/home/rotoapanta/Documentos/Proyects/gpsNetRsProject/logs/error.log'
logging.basicConfig(filename=log_file, level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Función para verificar la conectividad de un host
def check_host_connectivity(ip):
    response_time = ping(ip)
    return response_time is not None, response_time


# Función para obtener el diccionario IP - Hostname
def get_ip_hostname_dict():
    config = configparser.ConfigParser()
    config.read('config.ini')
    zabbix_url = config.get('zabbix', 'zabbix_url')
    zabbix_user = config.get('zabbix', 'zabbix_user')
    zabbix_password = config.get('zabbix', 'zabbix_password')
    try:
        # Configura la conexión a tu servidor Zabbix
        zapi = ZabbixAPI(url=zabbix_url, user=zabbix_user, password=zabbix_password)

        # Encuentra el template por nombre
        template_name = "Template GPS Trimble NetRS"
        template = zapi.template.get(filter={"host": template_name})

        ip_hostname_dict = {}

        if not template:
            logger.error(f"No se encontró el template '{template_name}'")
        else:
            template_id = template[0]["templateid"]
            # Encuentra los hosts asociados al template
            hosts = zapi.host.get(templateids=[template_id], selectInterfaces=["ip", "host"])

            # Recopila las direcciones IP de los hosts y verifica su conectividad
            for host in hosts:
                for interface in host["interfaces"]:
                    ip = interface["ip"]
                    is_reachable, response_time = check_host_connectivity(ip)
                    if is_reachable:
                        hostname = host["host"]
                        ip_hostname_dict[ip] = hostname

        # Cierra la sesión
        zapi.user.logout()
        return ip_hostname_dict
    except Exception as e:
        logger.error(f"Error al obtener el diccionario IP - Hostname: {e}")
        return {}


# Función para obtener valores de un host
def obtener_valores(ip, arguments):
    results = {}  # Define 'results' antes del bloque 'try'
    try:
        url_base = f'http://{ip}/prog/Show?'
        config = configparser.ConfigParser()
        config.read('config.ini')
        username = config.get('digitizer_credentials', 'username')
        password = config.get('digitizer_credentials', 'password')
        auth = (username, password)
        results = {}  # Diccionario para almacenar los resultados

        for argument in arguments:
            full_url = f"{url_base}{argument}"
            try:
                response = requests.get(full_url, auth=auth)
                response.raise_for_status()
                response_text = response.text

                patterns = {
                    "SystemName": r'name=(\w+)',
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
