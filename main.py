import requests
import re
from api_zbx_processing import get_ip_hostname_dict, obtener_valores  # Importa la función de zabbix.py


# Llamada a la función para obtener el diccionario IP - Hostname
ip_hostname_dict = get_ip_hostname_dict()

# Definición de los argumentos comunes como cadena
arguments = ["SystemName", "SerialNumber", "Voltage&input=2", "Temperature"]

# Itera a través de las direcciones IP y obtiene los valores de cada host
for ip, hostname in ip_hostname_dict.items():
    print(f"Valores para host {hostname} ({ip}):")

    values = obtener_valores(ip, arguments)
    print(f"values {values}")
    if values:
        for key, value in values.items():
            print(f"{key}: {value}")
    else:
        print("Error al hacer la solicitud HTTP: 404 Client Error: Not Found")
