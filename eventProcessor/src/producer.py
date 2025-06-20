import paho.mqtt.client as mqtt
import os
import json
import time
import random
from datetime import datetime, timezone

# Configurações do Broker MQTT
# Configurações (preferencialmente via variáveis de ambiente)
MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "localhost") # Use 'rabbitmq' se rodar o script fora de um container na mesma rede docker
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "weather/data") # Tópico para se inscrever
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "user")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "password")

# Cidades de exemplo
CITIES = ["New York", "London", "Tokyo", "Sao Paulo", "Paris", "Berlin"]
WIND_DIRECTIONS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]


def generate_random_weather_data():
    """Gera dados meteorológicos aleatórios."""
    now = datetime.now(timezone.utc)
    return {
        "timestamp": now.isoformat(timespec='seconds'),  # Corrigido de "timestap" para "timestamp"
        "city": random.choice(CITIES),
        "date": now.strftime("%Y-%m-%d"),
        "temperature": round(random.uniform(-10, 40), 1),  # Temperatura em Celsius
        "humidity": random.randint(20, 100),  # Umidade em %
        "windSpeed": round(random.uniform(0, 50), 1),  # Velocidade do vento em km/h
        "windDirection": random.choice(WIND_DIRECTIONS),
        "precipitation": round(random.uniform(0, 25), 1),  # Precipitação em mm
        "pressure": random.randint(980, 1050)  # Pressão em hPa
    }


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"Conectado ao Broker MQTT: {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}")
    else:
        print(f"Falha ao conectar, código de retorno: {rc}")


def on_publish(client, userdata, mid, reason_code, properties): # Assinatura atualizada
    # O parâmetro reason_code é um objeto MqttReasonCode, não um int simples para MQTT_ERR_SUCCESS
    # Para verificar o sucesso, comparamos com o valor numérico ou usamos o próprio objeto
    # No entanto, a mensagem de sucesso já é tratada no loop principal após client.publish()
    # Esta função é mais para logging ou ações adicionais após a confirmação do broker.
    print(f"Mensagem {mid} publicada com código de razão: {reason_code}")


def main():
    # Especifica a versão da API de callback para evitar DeprecationWarning
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
    client.on_connect = on_connect
    client.on_publish = on_publish

    # Descomente as linhas abaixo se o seu broker MQTT exigir autenticação
    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    try:
        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
    except Exception as e:
        print(f"Não foi possível conectar ao broker MQTT: {e}")
        return

    client.loop_start()  # Inicia o loop em uma thread separada

    try:
        while True:
            weather_payload = generate_random_weather_data()
            payload_json = json.dumps(weather_payload)

            result = client.publish(MQTT_TOPIC, payload_json)
            result.wait_for_publish()  # Espera a confirmação da publicação

            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"Publicado no tópico '{MQTT_TOPIC}': {payload_json}")
            else:
                print(f"Falha ao publicar mensagem no tópico '{MQTT_TOPIC}', erro: {mqtt.error_string(result.rc)}")

            time.sleep(5)  # Intervalo entre publicações (5 segundos)
    except KeyboardInterrupt:
        print("Publicação interrompida pelo usuário.")
    finally:
        client.loop_stop()
        client.disconnect()
        print("Desconectado do broker MQTT.")


if __name__ == "__main__":
    main()