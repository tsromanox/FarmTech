#include <Arduino.h>
// #include <PubSubClient.h> // Incluído via mqtt_client.h
// #include "config.h" // MQTT_BROKER, MQTT_PORT, MQTT_TOPIC serão passados como parâmetros ou definidos em config.h e incluídos onde necessário
#include "mqtt_client.h"

// O construtor agora recebe uma referência para PubSubClient
MQTTClient::MQTTClient(PubSubClient& pubSubClient) : mqttLibClient(pubSubClient) {
    // O PubSubClient já foi inicializado com o client de rede na sua construção.
}

void MQTTClient::messageCallback(char* topic, byte* payload, unsigned int length) {
    Serial.print("Message arrived [");
    Serial.print(topic);
    Serial.print("] ");
    for (unsigned int i = 0; i < length; i++) {
        Serial.print((char)payload[i]);
    }
    Serial.println();
    // Adicione aqui a lógica para processar a mensagem recebida
}

void MQTTClient::connect(const char* broker, uint16_t port, const char* clientId, const char* username, const char* password) {
    mqttLibClient.setServer(broker, port);
    mqttLibClient.setCallback(MQTTClient::messageCallback); // Define a função de callback para mensagens recebidas
    while (!mqttLibClient.connected()) {
        Serial.print("Attempting MQTT connection...");
        bool connectedStatus;
        if (username && password) {
            connectedStatus = mqttLibClient.connect(clientId, username, password);
        } else {
            connectedStatus = mqttLibClient.connect(clientId);
        }
        if (connectedStatus) {
            Serial.println(" connected");
        } else {
            Serial.print("failed, rc=");
            Serial.print(mqttLibClient.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }
}

void MQTTClient::publish(const char* topic, const String& jsonString) {
    mqttLibClient.publish(topic, jsonString.c_str());
}

void MQTTClient::subscribe(const char* topic) {
    mqttLibClient.subscribe(topic);
}

void MQTTClient::loop() {
    mqttLibClient.loop();
}

bool MQTTClient::connected() {
    return mqttLibClient.connected();
}