import logging
import os
from pyzabbix import ZabbixMetric, ZabbixSender
import datetime

# Obtiene la fecha actual en el formato deseado (Año-Mes-Día)
current_date = datetime.date.today().strftime("%Y-%m-%d")
# Obtiene la ruta completa al archivo de registro 'error.log' en la carpeta 'logs'
logs_folder = 'logs'
if not os.path.exists(logs_folder):
    os.makedirs(logs_folder)
# Nombre del archivo de registro con fecha
log_file = os.path.join(logs_folder, f'{current_date}_gps_netrs.log')
# Configura el sistema de registro de errores
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %('
                                                                   'message)s')
logger = logging.getLogger(__name__)


# Enviar las métricas a Zabbix
def send_data_to_zabbix(zabbix_server, zabbix_port, all_data):
    metrics = []

    for host, data in all_data.items():
        # Obtener los valores para esta estación
        station_code = data['station.code']
        serial_number = data['serial.number']
        input_voltage = data['input.voltage']
        system_temp = data['system.temp']

        # Crear métricas para cada valor
        metrics.append(ZabbixMetric(host, 'station.code', station_code))
        metrics.append(ZabbixMetric(host, 'serial.number', serial_number))
        metrics.append(ZabbixMetric(host, 'input.voltage', input_voltage))
        metrics.append(ZabbixMetric(host, 'system.temp', system_temp))

    try:
        # Crear un objeto ZabbixSender y enviar los datos a Zabbix
        zabbix_sender = ZabbixSender(zabbix_server=zabbix_server, zabbix_port=zabbix_port)
        result = zabbix_sender.send(metrics)
        logging.info(f"Datos enviados a Zabbix: {result}")
    except Exception as e:
        logging.error(f"Error al enviar datos a Zabbix: {e}")
