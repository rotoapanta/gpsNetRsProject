# Debes estar en el directorio raíz gpsNetRsProject y ejecutar el comando de prueba de la siguiente manera:
# (gps_netrs_env) rotoapanta@pc-linux:~/Documentos/Proyects/gpsNetRsProject$ python -m unittest tests.test_gps_netrs_project

import unittest
from api.api_zbx_processing import get_ip_hostname_dict, get_values
from zabbix_sender import send_data_to_zabbix


class TestGPSNetRsProject(unittest.TestCase):
    def test_get_ip_hostname_dict(self):
        # Llama a get_ip_hostname_dict
        result = get_ip_hostname_dict()

        # Verifica si result es un diccionario no vacío
        self.assertIsInstance(result, dict)
        self.assertTrue(len(result) > 0)

        # Verifica que los valores en el diccionario sean válidos
        for ip, hostname in result.items():
            self.assertIsInstance(ip, str)
            self.assertIsInstance(hostname, str)

        # Agrega más casos de prueba según sea necesario

    def test_get_values(self):
        # Llama a get_values con una IP y argumentos válidos
        result = get_values("192.168.6.103", ["SystemName", "SerialNumber"])

        # Verifica si result es un diccionario con datos válidos
        self.assertIsInstance(result, dict)
        self.assertIn("station.code", result)
        self.assertIn("serial.number", result)

        # Verifica el manejo de errores
        result = get_values("192.168.6.103", ["InvalidArgument"])
        self.assertIsInstance(result, dict)
        self.assertFalse(result)  # Debería ser un diccionario vacío

        # Agrega más casos de prueba según sea necesario

    def test_send_data_to_zabbix(self):
        # Define datos válidos para enviar
        all_data = {
            "RIOP_GP": {"station.code": "RIOP", "serial.number": "4927175199"},
            "CYRF_GP": {"station.code": "CYRF", "serial.number": "4805144946"},
        }

        # Llama a send_data_to_zabbix y verifica si se envían los datos
        zabbix_server = "http://192.168.1.115/zabbix"
        zabbix_port = 10051
        # Agrega claves "input.voltage" y "system.temp" a los datos
        all_data["RIOP_GP"]["input.voltage"] = "5.0"
        all_data["RIOP_GP"]["system.temp"] = "5.0"
        all_data["CYRF_GP"]["input.voltage"] = "4.8"
        all_data["CYRF_GP"]["system.temp"] = "6.5"
        send_data_to_zabbix(zabbix_server, zabbix_port, all_data)

        # Agrega más casos de prueba según sea necesario


if __name__ == '__main__':
    unittest.main()
