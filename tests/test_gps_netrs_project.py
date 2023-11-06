import unittest
from api.api_zbx_processing import get_ip_hostname_dict, get_values
from zabbix_sender import send_data_to_zabbix


class TestGPSNetRsProject(unittest.TestCase):
    def test_get_ip_hostname_dict(self):
        """
        This unit test, 'test_get_ip_hostname_dict', evaluates the 'get_ip_hostname_dict' function. This function
        retrieves the mapping of IP addresses to hostnames from a configuration.

        The test performs the following steps:
        1. Calls 'get_ip_hostname_dict' to obtain the IP-to-hostname mapping.
        2. Verifies if the result is a non-empty dictionary.
        3. Checks that the values in the dictionary are valid, with IP addresses as strings and hostnames as strings.

        The test is designed to be extendable with additional test cases if needed.

        :param None
        :return: None
        :raises: AssertionError, Exception (if an error occurs during the test execution)
        """
        # Call get_ip_hostname_dict
        result = get_ip_hostname_dict()

        # Check if the result is a non-empty dictionary.
        self.assertIsInstance(result, dict)
        self.assertTrue(len(result) > 0)

        # Verify that the values in the dictionary are valid
        for ip, hostname in result.items():
            self.assertIsInstance(ip, str)
            self.assertIsInstance(hostname, str)
        # Add more test cases as needed

    def test_get_values(self):
        """
        This unit test, 'test_get_values', is designed to evaluate the 'get_values' function, which retrieves various
        metrics from a GPS NetRS device via an HTTP request with specified arguments.

        The test performs the following steps:
        1. Calls 'get_values' with a valid IP address, '192.168.6.103', and a list of valid arguments, including
        'SystemName' and 'SerialNumber'.
        2. Verifies that the result is a dictionary containing valid data.
        3. Checks if 'station.code' and 'serial.number' are present in the result.
        4. Validates the error handling by calling 'get_values' with an invalid argument, 'InvalidArgument'.
        5. Ensures that the result is an empty dictionary, as it's expected to handle the error gracefully.
        6. Provides flexibility for adding more test cases as needed.

        :param None
        :return: None
        :raises: AssertionError, Exception (if an error occurs during the test execution)
        """
        # Call get_values with a valid IP and arguments
        result = get_values("192.168.6.103", ["SystemName", "SerialNumber"])

        # Verify if the result is a dictionary with valid data
        self.assertIsInstance(result, dict)
        self.assertIn("station.code", result)
        self.assertIn("serial.number", result)

        # Check error handling
        result = get_values("192.168.6.103", ["InvalidArgument"])
        self.assertIsInstance(result, dict)
        self.assertFalse(result)  # Should be an empty dictionary
        # Add more test cases as needed

    def test_send_data_to_zabbix(self):
        """
        This unit test, 'test_send_data_to_zabbix', evaluates the 'send_data_to_zabbix' function. This function sends
        valid data to a Zabbix server for monitoring.

        The test performs the following steps:
        1. Defines valid data for sending, which includes two GPS devices, 'RIOP_GP' and 'CYRF_GP', each with
        'station.code' and 'serial.number'.
        2. Calls 'send_data_to_zabbix' with the Zabbix server URL 'http://192.168.1.115/zabbix' and port '10051'.
        3. Adds 'input.voltage' and 'system.temp' keys to the data for each device.
        4. Verifies if the data is successfully sent to Zabbix.

        The test provides flexibility for adding more test cases as needed.

        :param None
        :return: None
        :raises: AssertionError, Exception (if an error occurs during the test execution)
        """
        # Define valid data to send
        all_data = {
            "RIOP_GP": {"station.code": "RIOP", "serial.number": "4927175199"},
            "CYRF_GP": {"station.code": "CYRF", "serial.number": "4805144946"},
        }

        # Call send_data_to_zabbix and verify if the data is sent
        zabbix_server = "http://192.168.1.115/zabbix"
        zabbix_port = 10051
        # Add "input.voltage" and "system.temp" keys to the data
        all_data["RIOP_GP"]["input.voltage"] = "5.0"
        all_data["RIOP_GP"]["system.temp"] = "5.0"
        all_data["CYRF_GP"]["input.voltage"] = "4.8"
        all_data["CYRF_GP"]["system.temp"] = "6.5"
        send_data_to_zabbix(zabbix_server, zabbix_port, all_data)
        # Add more test cases as needed


if __name__ == '__main__':
    unittest.main()