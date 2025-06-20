# FarmTechIOT - Sistema de Monitoramento e Irrigação

Este projeto implementa um sistema de IoT para monitoramento de condições ambientais (temperatura e umidade) e controle automatizado de irrigação para pequenas plantações ou jardins. Utiliza um microcontrolador ESP32, um sensor DHT22, um display LCD I2C e um módulo relé para controlar uma bomba d'água.

## Funcionalidades Principais

-   **Monitoramento em Tempo Real:** Leitura contínua dos dados de temperatura e umidade do ambiente.
-   **Display Local:** Exibição das informações em um display LCD 20x4, incluindo leituras dos sensores, status da bomba e hora atual.
-   **Irrigação Automatizada:** Acionamento automático de uma bomba d'água (através de um relé) quando a umidade do ar cai abaixo de um limiar pré-definido.
-   **Conectividade Wi-Fi:** Conecta-se a uma rede Wi-Fi para acesso a serviços de rede.
-   **Sincronização de Horário:** Obtém a data e hora atuais de um servidor NTP (Network Time Protocol).
-   **Publicação de Dados (Opcional):** Envia os dados dos sensores em formato JSON para um broker MQTT, permitindo monitoramento remoto, armazenamento de histórico e integração com outras plataformas de IoT.

## Componentes de Hardware

-   Placa de Desenvolvimento ESP32
-   Sensor de Temperatura e Umidade DHT22
-   Display LCD I2C 20x4
-   Módulo Relé de 1 Canal (5V)
-   LED para feedback visual
-   Protoboard e Jumpers

## Estrutura do Projeto

O código está organizado nos seguintes arquivos principais:

-   `src/main.cpp`: Contém a lógica principal da aplicação, incluindo a inicialização (`setup()`) e o loop de execução (`loop()`). É responsável por ler os sensores, controlar o display, gerenciar a lógica da bomba e coordenar a comunicação MQTT.
-   `include/config.h`: Arquivo central de configurações. Nele são definidos parâmetros como credenciais de Wi-Fi, detalhes do broker MQTT, pinos de conexão dos componentes (sensores, atuadores) e configurações do display.
-   `src/mqtt_client.cpp` e `include/mqtt_client.h`: Abstraem a comunicação com o broker MQTT. A classe `MQTTClient` encapsula a biblioteca `PubSubClient`, simplificando as operações de conexão, publicação e recebimento de mensagens.

## Funcionamento Detalhado

### 1. Inicialização (`setup()`)

Ao ser ligado, o ESP32 executa as seguintes rotinas de inicialização:

1.  **Comunicação:** Inicia a comunicação Serial (para depuração), I2C (para o LCD) e define os pinos (GPIOs) como entrada ou saída.
2.  **Display LCD:** Inicializa o display e liga a luz de fundo.
3.  **Conexão Wi-Fi:** Tenta se conectar à rede Wi-Fi definida em `config.h`. Um ícone de "spinner" é exibido no LCD durante o processo.
4.  **Sensor DHT:** Inicializa o sensor de temperatura e umidade.
5.  **Sincronização de Horário:** Configura e sincroniza o relógio interno com um servidor NTP.
6.  **Conexão MQTT (se ativado):** Caso a diretiva `USE_MQTT_BROKER` esteja definida como `1` em `config.h`, o sistema se conecta ao broker MQTT especificado.

### 2. Loop Principal (`loop()`)

O loop principal é executado continuamente e é baseado em um temporizador não-bloqueante (`millis()`) para realizar as tarefas a cada 1 segundo.

1.  **Leitura dos Sensores:** A cada intervalo, o sistema lê os valores de umidade e temperatura do sensor DHT22.
2.  **Lógica de Controle da Bomba:**
    -   O valor de umidade é verificado. No código atual, o limiar é de `50.0%`.
    -   Se a umidade for inferior a 50% (e a leitura for válida), a variável `activate_pump` se torna `true`, e o pino do relé é acionado (`HIGH`), ligando a bomba.
    -   Caso contrário, o pino do relé é desativado (`LOW`), desligando a bomba.
3.  **Atualização do Display:**
    -   O status da bomba ("Ligada" ou "Desligada") é exibido na primeira linha.
    -   Os valores de umidade e temperatura são exibidos nas linhas seguintes.
    -   A data e a hora atuais são exibidas na última linha.
4.  **Comunicação MQTT (se ativado):**
    -   Verifica se a conexão com o broker MQTT está ativa. Se não estiver, tenta reconectar.
    -   Cria uma string no formato JSON contendo os dados de umidade, temperatura e um timestamp (atualmente um placeholder).
    -   Publica essa string JSON no tópico MQTT definido em `config.h`.

## Como Configurar e Usar

1.  **Configuração do Ambiente:**
    -   Tenha o PlatformIO instalado no seu VS Code ou use a IDE do Arduino.
    -   Instale as bibliotecas necessárias:
        -   `LiquidCrystal_I2C`
        -   `DHT sensor library` by Adafruit
        -   `PubSubClient` by Nick O'Leary

2.  **Arquivo `config.h`:**
    -   Abra o arquivo `/include/config.h`.
    -   Altere as macros `WIFI_SSID` e `WIFI_PASSWORD` com as credenciais da sua rede Wi-Fi.
    -   Para usar a funcionalidade MQTT, mude `#define USE_MQTT_BROKER 0` para `#define USE_MQTT_BROKER 1`.
    -   Se estiver usando MQTT, configure os dados do seu broker: `MQTT_BROKER_ADDRESS`, `MQTT_BROKER_PORT`, `MQTT_TOPIC`, `MQTT_USERNAME` e `MQTT_PASSWORD`.
    -   Verifique se os pinos definidos (`I2C_SDA`, `I2C_SCL`, `DHTPIN`, `RELAY_PIN`, `LED_PIN`) correspondem à sua montagem física.

3.  **Compilação e Upload:**
    -   Conecte o ESP32 ao seu computador.
    -   Compile e faça o upload do código usando o PlatformIO ou a IDE do Arduino.
    -   Abra o Monitor Serial para acompanhar os logs de conexão e os dados dos sensores.