#ifndef MQTT_CLIENT_H
#define MQTT_CLIENT_H

#include <PubSubClient.h>
#include <Client.h> // Necessário para o parâmetro do construtor

class MQTTClient {
public:
    MQTTClient(PubSubClient& pubSubClient); // Declaração corrigida do construtor
    //MQTTClient(Client& client, PubSubClient& pubSubClient);
    void connect(const char* broker, uint16_t port, const char* clientId, const char* username = nullptr, const char* password = nullptr);
    void publish(const char* topic, const String& jsonString);
    void subscribe(const char* topic);
    void loop();
    bool connected();

private:
    static void messageCallback(char* topic, byte* payload, unsigned int length);
    PubSubClient& mqttLibClient; // Renomeado para evitar confusão e usar referência
};

#endif // MQTT_CLIENT_H