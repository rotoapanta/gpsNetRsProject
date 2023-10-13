# Diccionario IP - Hostname:
# IP: 192.168.16.110, Hostname: PLHA_GP
# IP: 192.168.16.111, Hostname: CCNE_GP
# IP: 192.168.16.107, Hostname: CUIC_GP
import re

import requests
from pyzabbix.api import ZabbixAPI
from ping3 import ping


# Función para verificar la conectividad de un host
def check_host_connectivity(ip):
    response_time = ping(ip)
    if response_time is not None:
        return True, response_time
    else:
        return False, None


# Función para obtener el diccionario IP - Hostname
def get_ip_hostname_dict():
    # Configura la conexión a tu servidor Zabbix
    zapi = ZabbixAPI(url='http://192.168.1.115/zabbix', user='rtoapanta', password='TECNOLOGO')

    # Encuentra el template por nombre
    template_name = "Template GPS Trimble NetRS"
    template = zapi.template.get(filter={"host": template_name})

    ip_hostname_dict = {}

    if not template:
        print(f"No se encontró el template '{template_name}'")
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

def obtener_valores(ip, arguments):
    url_base = f'http://{ip}/prog/Show?'

    # Aquí se proporcionan las credenciales de usuario y contraseña
    auth = ('sysadmin', 'instituto')

    results = {}  # Diccionario para almacenar los resultados

    for argument in arguments:
        full_url = f"{url_base}{argument}"
        response = requests.get(full_url, auth=auth)
        response_text = response.text

        # Expresiones regulares para buscar los valores deseados
        patterns = {
            "SystemName": r'name=(\w+)',
            "SerialNumber": r'sn=(\d+)',
            "Voltage&input=2": r'volts=([\d.]+)',
            "Temperature": r'temp=(\d+)'
        }

        for arg, pattern in patterns.items():
            match = re.search(pattern, response_text)
            if match:
                results[arg] = match.group(1)

    return results  # Devuelve un diccionario con los resultados