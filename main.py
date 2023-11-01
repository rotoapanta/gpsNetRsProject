import configparser
import logging
import os
from api.api_zbx_processing import get_ip_hostname_dict, get_values
from zabbix_sender import send_data_to_zabbix
import datetime


def main():
    """
    The 'main' function serves as the entry point of the GPS NetRS monitoring program. It performs the following tasks:
    1. Obtains the current date in the desired format (Year-Month-Day).
    2. Configures the error logging system and creates log files.
    3. Calls the 'get_ip_hostname_dict' function to retrieve the IP - Hostname dictionary.
    4. Defines a list of common arguments as strings.
    5. Creates a dictionary to store data for each host.
    6. Iterates through the IP - Hostname dictionary, calling 'get_values' function for each host and collecting data.
    7. Reads Zabbix configuration from 'config.ini'.
    8. Sends collected data to Zabbix using the 'send_data_to_zabbix' function.
    9. Logs errors and completion messages.

    This function does not accept any parameters.

    :returns: None
    :raises: subprocess.CalledProcessError (if command execution fails), Exception (if any other error occurs during
    execution)
    """
    # Obtiene la fecha actual en el formato deseado (Año-Mes-Día)
    fecha_actual = datetime.date.today().strftime("%Y-%m-%d")
    # Obtiene la ruta completa al archivo de registro 'error.log' en la carpeta 'logs'
    logs_folder = 'logs'
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)
    # Nombre del archivo de registro con fecha
    log_file = os.path.join(logs_folder, f'{fecha_actual}_gps_netrs.log')
    # Configura el sistema de registro de errores
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %('
                                                                       'message)s')
    logger = logging.getLogger(__name__)

    logger.info("Inicio del programa")  # Agrega un mensaje de inicio
    try:
        # Llamada a la función para obtener el diccionario IP - Hostname
        ip_hostname_dict = get_ip_hostname_dict()

        # Definición de los argumentos comunes como cadena
        arguments = ["SystemName", "SerialNumber", "Voltage&input=2", "Temperature"]

        # Crear un diccionario para almacenar los datos de cada host
        all_data = {}

        for ip, hostname in ip_hostname_dict.items():
            try:
                data = get_values(ip, arguments)
                if data:
                    all_data[hostname] = data
                else:
                    logger.error(f"Error al obtener valores para {hostname} ({ip})")
            except Exception as e:
                logger.error(f"Error al obtener valores para {hostname} ({ip}): {e}")

        # Leer la configuración de Zabbix desde config.ini
        config = configparser.ConfigParser()
        config.read('config.ini')

        zabbix_server = config.get('zabbix', 'zabbix_server')
        zabbix_port = int(config.get('zabbix', 'zabbix_port'))

        try:
            # Enviar datos a Zabbix utilizando el script "zabbix.py"
            send_data_to_zabbix(zabbix_server, zabbix_port, all_data)
        except Exception as e:
            logger.error(f"Error al enviar datos a Zabbix: {e}")
    except Exception as e:
        logger.error(f"Error en la ejecución principal: {e}")
    finally:
        logger.info("Fin del programa")  # Agrega un mensaje de finalización


if __name__ == "__main__":
    main()
