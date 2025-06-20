#include "config.h" 

#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h> 
#include <WiFi.h>

#if USE_MQTT_BROKER
#include <PubSubClient.h>
#include "mqtt_client.h"
#endif

// Inicializa dependencias
LiquidCrystal_I2C lcd(I2C_ADDR, LCD_COLUMNS, LCD_ROWS);
DHT dht(DHTPIN, DHTTYPE);

unsigned long previousMillis = 0;  // Armazena o último valor de millis
const long interval = 1000;  // Intervalo de 1 segundo (1000 ms)

 bool activate_pump = false; // Variável para ativar/desativar a bomba

#if USE_MQTT_BROKER
WiFiClient net_client; // Cliente de rede padrão
PubSubClient pubsub_client_instance(net_client);
MQTTClient mqtt_service_client(pubsub_client_instance); // Corrigido: construtor espera apenas pubsub_client_instance
#endif

void spinner() {
  static int8_t counter = 0;
  const char* glyphs = "\xa1\xa5\xdb";
  lcd.setCursor(15, 1);
  lcd.print(glyphs[counter++]);
  if (counter == strlen(glyphs)) {
    counter = 0;
  }
}

void printLocalTime() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    lcd.setCursor(0, 3);
    lcd.println("Connection Err");
    return;
  }
  lcd.setCursor(0, 3);
  lcd.println(&timeinfo, "%d/%m/%Y %H:%M:%S");
}

void setup() {
  Serial.begin(115200);
  // Inicializa a comunicação I2C com os pinos definidos
  Wire.begin(I2C_SDA, I2C_SCL);
    
  lcd.begin(LCD_COLUMNS, LCD_ROWS);  // Inicializa o LCD com o número de colunas e linhas
  lcd.backlight();  // Liga a luz de fundo do LCD
  lcd.setCursor(0, 0);  // Posiciona o cursor na primeira coluna da primeira linha
  //lcd.print("Contagem:");  // Exibe a mensagem

  lcd.print("Connecting to WiFi");

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD, 6);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    spinner();
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  dht.begin();
  pinMode(LED_PIN, OUTPUT);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW); // Bomba desligada inicialmente
  digitalWrite(LED_PIN, LOW);   // LED desligado inicialmente

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.println("Online");
  lcd.setCursor(0, 1);
  lcd.println("Updating time...");
  configTime(UTC_OFFSET, UTC_OFFSET_DST, NTP_SERVER);
  #if USE_MQTT_BROKER
  // Configuração do cliente MQTT
    mqtt_service_client.connect(MQTT_BROKER_ADDRESS, MQTT_BROKER_PORT, "DHTClientMain", MQTT_USERNAME, MQTT_PASSWORD);
  #endif
  lcd.setCursor(0, 0);
  lcd.println("Online");
}

void loop() {
    #if USE_MQTT_BROKER
      if (!mqtt_service_client.connected()) {
        Serial.println("MQTT Desconectado. Tentando reconectar...");
        // Configuração do cliente MQTT
        mqtt_service_client.connect(MQTT_BROKER_ADDRESS, MQTT_BROKER_PORT, "DHTClientMain_Reconnect", MQTT_USERNAME, MQTT_PASSWORD);
      }
      mqtt_service_client.loop();
    #endif

    digitalWrite(LED_PIN, HIGH);   // Ligar LED
    unsigned long currentMillis = millis();  // Pega o tempo atual
    String timestamp = "2023-10-27T10:30:00Z"; // Obter o timestamp atual (placeholder)

    // Verifica se já passou 1 segundo (1000 ms)
    if (currentMillis - previousMillis >= interval) {
        previousMillis = currentMillis;  // Atualiza o valor de previousMillis
            float humidity = dht.readHumidity();
            float temperature = dht.readTemperature(); // DHT22
            // Verifica se as leituras são válidas (não NaN)
            if (isnan(humidity) || isnan(temperature)) {
              Serial.println("Falha ao ler do sensor DHT!");
              digitalWrite(LED_PIN, LOW);    // Desligar LED em caso de falha
              delay(2000); // Aguarda antes de tentar novamente
              return;
            }
            // Cria a string JSON
            String jsonString = "{\"timestamp\": \"" + timestamp + "\"," +
                      "\"humidity\": " + String(humidity) + "," +
                      "\"temperature_C\": " + String(temperature) + "}";
            Serial.println(jsonString);
            lcd.setCursor(0, 1);  // Posiciona o cursor na primeira coluna da segunda linha
            //lcd.print("              ");  // Limpa a linha anterior (apaga números antigos aplicando espaços vazios)
            lcd.setCursor(0, 1);  // Reposiciona o cursor
            lcd.print("humidity:" + String(humidity));
            lcd.setCursor(0, 2);  // Posiciona o cursor na segunda coluna da segunda linha
            //lcd.print("              ");  // Limpa a linha anterior (apaga números antigos aplicando espaços vazios)
            lcd.setCursor(0, 2);  // Reposiciona o cursor
            lcd.print("temperature:" + String(temperature) + "C");
            #if USE_MQTT_BROKER
            if (mqtt_service_client.connected()) {
                Serial.println("Enviando dados para o MQTT Broker...");
                mqtt_service_client.publish(MQTT_TOPIC, jsonString.c_str());
            } else {
                Serial.println("MQTT não está conectado. Tentando reconectar...");
                mqtt_service_client.connect(MQTT_BROKER_ADDRESS, MQTT_BROKER_PORT, "DHTClientMain_Reconnect", MQTT_USERNAME, MQTT_PASSWORD);
            }
            #endif
            if (humidity < 50.0 && humidity > 0) { // Adicionado humidity > 0 para evitar ligar com NaN
                activate_pump = true;
            } else {
                activate_pump = false;
            }
            if (activate_pump) {
                digitalWrite(RELAY_PIN, HIGH); // Liga a bomba
                lcd.setCursor(0, 0);
                lcd.print("Bomba: Ligada   ");
                Serial.println("Bomba ligada");
            } else {
                digitalWrite(RELAY_PIN, LOW); // Desliga a bomba
                lcd.setCursor(0, 0);
                lcd.print("Bomba: Desligada");
                Serial.println("Bomba desligada");
            }
            //digitalWrite(LED_PIN, LOW);    // Desligar LED após enviar os dados
    }
    printLocalTime();
}
