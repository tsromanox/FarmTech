import paho.mqtt.client as mqtt
import ssl
import json
import os
import time
import certifi

# Configure o Python para usar os certificados CA do certifi
os.environ["SSL_CERT_FILE"] = certifi.where()

# --- Configurações para Azure IoT Hub ---
IOT_HUB_NAME = os.getenv("IOT_HUB_NAME", "tsx-brs-iot001")
DEVICE_ID = os.getenv("DEVICE_ID", "device01")
SAS_TOKEN_STR = os.getenv("SAS_TOKEN", "b1TISL3FB9pDZX0IlAkElqKDZhDzDujFCwfJSmr8C4A=")  # Cole o token SAS gerado aqui

if not SAS_TOKEN_STR:
    print("Erro: SAS_TOKEN não definido nas variáveis de ambiente.")
    exit()

MQTT_BROKER_HOST = f"{IOT_HUB_NAME}.azure-devices.net"
MQTT_BROKER_PORT = 8883  # MQTTS
MQTT_USERNAME = f"{MQTT_BROKER_HOST}/{DEVICE_ID}/?api-version=2021-04-12"
MQTT_PASSWORD = SAS_TOKEN_STR
CLIENT_ID = DEVICE_ID

# Tópico para receber mensagens Cloud-to-Device (C2D)
MQTT_TOPIC_C2D = f"devices/{DEVICE_ID}/messages/devicebound/#"


# Seu código de conexão ao MongoDB pode permanecer aqui se você quiser armazenar as mensagens C2D
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
# MONGO_DATABASE = os.getenv("MONGO_DATABASE", "trainstormdb")
# MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "c2d_events")
# mongo_client_instance = None
# db_collection = None

# def connect_to_mongodb(): ... (seu código aqui)

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"Conectado ao Azure IoT Hub: {MQTT_BROKER_HOST}")
        client.subscribe(MQTT_TOPIC_C2D)
        print(f"Inscrito no tópico C2D: {MQTT_TOPIC_C2D}")
    else:
        print(f"Falha ao conectar ao Azure IoT Hub, código de retorno: {rc}")


def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Mensagem C2D recebida do tópico '{msg.topic}': {payload}")
    try:
        data = json.loads(payload)
        # Faça algo com a mensagem C2D, por exemplo, acionar uma ação no dispositivo
        # Se quiser salvar no MongoDB:
        # if db_collection is not None:
        #     db_collection.insert_one(data)
        #     print(f"Dados C2D inseridos no MongoDB: {data}")
        # else:
        #     print("Coleção MongoDB não está disponível. Mensagem C2D não armazenada.")
        print(f"Dados C2D processados: {data}")
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON da mensagem C2D: {payload}")
    except Exception as e:
        print(f"Erro ao processar mensagem C2D: {e}")


def consume_c2d_from_iot_hub():
    # connect_to_mongodb() # Descomente se for usar MongoDB

    mqtt_client = mqtt.Client(client_id=CLIENT_ID, callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
                              protocol=mqtt.MQTTv5)
    mqtt_client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
    mqtt_client.tls_set(tls_version=ssl.PROTOCOL_TLS_CLIENT)

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    retry_delay = 5
    while True:
        try:
            print(f"Tentando conectar ao Azure IoT Hub em {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}...")
            mqtt_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
            break
        except Exception as e:
            print(f"Falha na conexão MQTT com Azure IoT Hub: {e}. Tentando novamente em {retry_delay} segundos...")
            time.sleep(retry_delay)

    try:
        print("Aguardando mensagens Cloud-to-Device...")
        mqtt_client.loop_forever()
    except KeyboardInterrupt:
        print("Consumo C2D interrompido.")
    finally:
        mqtt_client.disconnect()
        # if mongo_client_instance:
        #     mongo_client_instance.close()
        print("Desconectado do Azure IoT Hub.")


if __name__ == "__main__":
    consume_c2d_from_iot_hub()
