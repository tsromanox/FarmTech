import certifi
import paho.mqtt.client as mqtt
import ssl
import json
import os
import time
import urllib.parse  # Para codificar propriedades no tópico

# --- Configurações para Azure IoT Hub ---
IOT_HUB_NAME = os.getenv("IOT_HUB_NAME", "tsx-brs-iot001")
DEVICE_ID = os.getenv("DEVICE_ID", "device01")
SAS_TOKEN_STR = os.getenv("SAS_TOKEN_STR", "7myi2PWJTM2lA6xOADWOPpAWpKjm1Yimqqwv5O4W5nc=")  # Cole o token SAS gerado aqui

if not SAS_TOKEN_STR:
    print("Erro: SAS_TOKEN não definido nas variáveis de ambiente.")
    exit()

MQTT_BROKER_HOST = f"{IOT_HUB_NAME}.azure-devices.net"
MQTT_BROKER_PORT = 8883  # MQTTS
MQTT_USERNAME = f"{MQTT_BROKER_HOST}/{DEVICE_ID}/?api-version=2021-04-12"
MQTT_PASSWORD = SAS_TOKEN_STR  # O token SAS completo
CLIENT_ID = DEVICE_ID

# Tópico para enviar mensagens Device-to-Cloud (D2C)
# Você pode adicionar propriedades customizadas codificadas na URL, ex: %24.ct=application%2Fjson&%24.ce=utf-8
MQTT_TOPIC_D2C = f"devices/{DEVICE_ID}/messages/events/"


# Exemplo com propriedades:
# properties = urllib.parse.urlencode({"prop1":"value1", "$contentType": "application/json", "$contentEncoding": "utf-8"})
# MQTT_TOPIC_D2C = f"devices/{DEVICE_ID}/messages/events/{properties}"


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"Conectado ao Azure IoT Hub: {MQTT_BROKER_HOST}")
    else:
        print(f"Falha ao conectar ao Azure IoT Hub, código de retorno: {rc}")
        # Códigos de erro comuns do IoT Hub:
        # 2: Identificador rejeitado (verifique ClientID)
        # 4: Usuário ou senha inválidos (verifique Username e SAS Token)
        # 5: Não autorizado (verifique SAS Token, políticas do IoT Hub)


def on_publish(client, userdata, mid, reason_code, properties):
    print(f"Mensagem {mid} publicada com código de razão: {reason_code}")


def send_data_to_iot_hub():
    mqtt_client = mqtt.Client(client_id=CLIENT_ID, callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
                              protocol=mqtt.MQTTv5)
    mqtt_client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)

    # Configuração TLS/SSL
    # Por padrão, paho-mqtt usa os certificados CA do sistema.
    # Se você precisar de um certificado específico (ex: Baltimore CyberTrust Root),
    # você pode especificá-lo com tls_set(ca_certs="path/to/baltimore.pem")
    mqtt_client.tls_set(certifi.where(), tls_version=ssl.PROTOCOL_TLS_CLIENT)
    # Opcional: para ignorar a verificação do hostname (não recomendado para produção)
    # mqtt_client.tls_insecure_set(True)

    mqtt_client.on_connect = on_connect
    mqtt_client.on_publish = on_publish

    try:
        print(f"Tentando conectar ao Azure IoT Hub em {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}...")
        mqtt_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
    except Exception as e:
        print(f"Falha na conexão MQTT com Azure IoT Hub: {e}")
        return

    mqtt_client.loop_start()
    count = 0
    try:
        while True:
            count += 1
            message_payload = {
                "deviceId": DEVICE_ID,
                "messageId": count,
                "temperature": 20 + (count % 10),
                "humidity": 60 + (count % 20)
            }
            payload_json = json.dumps(message_payload)

            result = mqtt_client.publish(MQTT_TOPIC_D2C, payload_json, qos=1)  # QoS 1 é recomendado
            result.wait_for_publish(timeout=5)

            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"Publicado no tópico '{MQTT_TOPIC_D2C}': {payload_json}")
            else:
                print(f"Falha ao publicar mensagem, erro: {mqtt.error_string(result.rc)}")

            time.sleep(10)  # Intervalo entre publicações
    except KeyboardInterrupt:
        print("Envio interrompido.")
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        print("Desconectado do Azure IoT Hub.")


if __name__ == "__main__":
    send_data_to_iot_hub()
