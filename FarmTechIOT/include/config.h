// This file contains configuration settings for the MQTT client
#ifndef CONFIG_H
#define CONFIG_H

// --- Seleção do Serviço MQTT ---
// Defina como 1 para usar Azure IoT Hub, 0 para usar o broker MQTT padrão.
#define USE_AZURE_IOT_HUB 0 // Mude para 1 para testar com Azure IoT Hub
#define USE_MQTT_BROKER 0 // Mude para 0 para desativar envio para Broker MQTT
// --- Configurações do Azure IoT Hub ---
#define MQTT_BROKER_ADDRESS "host.wokwi.internal"
#define MQTT_BROKER_PORT 1883
#define MQTT_TOPIC "sensor/data"
#define MQTT_USERNAME "user"   // Not required for test.mosquitto.org
#define MQTT_PASSWORD "password"   // Not required for test.mosquitto.org

// --- Configurações Wi-Fi ---
#define WIFI_SSID "Wokwi-GUEST"
#define WIFI_PASSWORD ""

// --- Configurações de NTP ---
#define NTP_SERVER     "pool.ntp.org"
#define UTC_OFFSET     0
#define UTC_OFFSET_DST 0
// --- Configurações do LCD ---

// Endereço I2C do módulo do LCD, normalmente 0x27 ou 0x3F
#define I2C_ADDR 0x27
#define LCD_COLUMNS 20
#define LCD_ROWS 4

// Definindo os pinos SCL e SDA para o ESP32
#define I2C_SDA 21  // Pino GPIO 21 para SDA
#define I2C_SCL 22  // Pino GPIO 22 para SCL
#endif // CONFIG_H

// --- Configurações do DHT Sensor ---
#define DHTPIN 15      // Pino de dados do DHT22
#define DHTTYPE DHT22  // Tipo do sensor DHT
// --- Configurações do LED ---
#define LED_PIN 23
// ---- RELE
#define RELAY_PIN 2