from pyzabbix import ZabbixMetric, ZabbixSender


# Enviar datos a Zabbix
def enviar_datos_zabbix(zabbix_server, zabbix_port, keys, data):
    # Obtener las métricas a enviar a Zabbix
    metrics = obtener_metricas_para_enviar(keys, data)
    # Imprimir las métricas
    imprimir_metricas(metrics)

    try:
        # Crear un objeto ZabbixSender y enviar los datos a Zabbix
        zabbix_sender = ZabbixSender(zabbix_server=zabbix_server, zabbix_port=zabbix_port)
        result = zabbix_sender.send(metrics)
        print(f"Datos enviados a Zabbix: {result}")
    except Exception as e:
        print(f"Error al enviar datos a Zabbix: {e}")


# Obtener las métricas a enviar a Zabbix
def obtener_metricas_para_enviar(keys, data):
    metrics = []

    for key, value in data.items():
        if key in keys:
            zabbix_key = keys[key]
            host = data['station.code']
            metrics.append(ZabbixMetric(host + '_QA', zabbix_key, value))

    return metrics


# Imprimir las métricas a enviar a Zabbix
def imprimir_metricas(metrics):
    print("Datos a enviar a Zabbix:")
    for item in metrics:
        print(f"Host: {item.host}, Key: {item.key}, Value: {item.value}")