import paho.mqtt.client as mqtt
import pymongo
import json
import os
import time

# Configurações (preferencialmente via variáveis de ambiente)
#MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "test.mosquitto.org") # Use 'rabbitmq' se rodar o script fora de um container na mesma rede docker
MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "127.0.0.1")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "sensor/data") # Tópico para se inscrever
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "user")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "password")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/") # Use 'mongodb://mongodb:27017/' se rodar o script em um container na mesma rede docker
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "trainstormdb")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "events")

mongo_client_instance = None
db_collection = None

def connect_to_mongodb():
    global mongo_client_instance, db_collection
    retry_delay = 5
    while True:
        try:
            print(f"Conectando ao MongoDB em {MONGO_URI}...")
            mongo_client_instance = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            mongo_client_instance.admin.command('ping') # Verifica a conexão
            db = mongo_client_instance[MONGO_DATABASE]
            db_collection = db[MONGO_COLLECTION]
            print(f"Conectado com sucesso ao MongoDB: DB='{MONGO_DATABASE}', Collection='{MONGO_COLLECTION}'.")
            break
        except pymongo.errors.ConnectionFailure as e:
            print(f"Falha na conexão com MongoDB: {e}. Tentando novamente em {retry_delay} segundos...")
            time.sleep(retry_delay)
        except Exception as e:
            print(f"Erro inesperado ao conectar ao MongoDB: {e}. Tentando novamente em {retry_delay} segundos...")
            time.sleep(retry_delay)

def on_connect(client, userdata, flags, rc, properties=None): # properties adicionado para compatibilidade com paho-mqtt v2+
    if rc == 0:
        print(f"Conectado ao Broker MQTT: {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}")
        client.subscribe(MQTT_TOPIC)
        print(f"Inscrito no tópico: {MQTT_TOPIC}")
    else:
        print(f"Falha ao conectar ao Broker MQTT, código de retorno: {rc}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Mensagem recebida do tópico '{msg.topic}': {payload}")
    try:
        data = json.loads(payload)
        if db_collection is not None:
            db_collection.insert_one(data)
            print(f"Dados inseridos no MongoDB: {data}")
        else:
            print("Coleção MongoDB não está disponível. Mensagem não armazenada.")
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON: {payload}")
    except Exception as e:
        print(f"Erro ao processar mensagem ou inserir no MongoDB: {e}")

def main():
    connect_to_mongodb()

    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5) # Especifica a versão da API de callback
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    # Adicione a configuração de usuário e senha aqui
    if MQTT_USERNAME and MQTT_PASSWORD:
        mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    retry_delay = 5
    while True:
        try:
            print(f"Tentando conectar ao broker MQTT em {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}...")
            mqtt_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
            break # Sai do loop se conectado com sucesso
        except Exception as e:
            print(f"Falha na conexão MQTT: {e}. Tentando novamente em {retry_delay} segundos...")
            time.sleep(retry_delay)

    try:
        mqtt_client.loop_forever()
    except KeyboardInterrupt:
        print("Desconectando...")
    finally:
        mqtt_client.disconnect()
        if mongo_client_instance:
            mongo_client_instance.close()
        print("Limpeza concluída.")

if __name__ == "__main__":
    main()