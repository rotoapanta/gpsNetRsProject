import subprocess
import logging
import os
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


# Función para verificar la conectividad de un host
def check_host_connectivity(ip):
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
