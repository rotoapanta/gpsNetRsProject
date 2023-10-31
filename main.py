import configparser
import logging
import os
from api.api_zbx_processing import get_ip_hostname_dict, get_values
from zabbix_sender import send_data_to_zabbix


def main():
    # Obtiene la ruta completa al archivo de registro 'error.log' en la carpeta 'logs'
    logs_folder = 'logs'
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)

    log_file = os.path.join(logs_folder, 'error.log')
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
