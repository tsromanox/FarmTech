# Processador de Eventos MQTT para MongoDB

## Descrição

Este projeto consiste em um consumidor MQTT escrito em Python que escuta mensagens em um tópico específico, processa essas mensagens (assumidas como JSON) e as armazena em uma coleção MongoDB. O sistema é projetado para ser resiliente, com tentativas de reconexão tanto para o broker MQTT quanto para o MongoDB, e é configurável através de variáveis de ambiente. Utiliza MQTT v5.

## Funcionalidades

*   **Consumidor MQTT**: Conecta-se a um broker MQTT e se inscreve em um tópico.
*   **Processamento de Mensagens**: Decodifica payloads de mensagens (esperado em formato JSON).
*   **Armazenamento em MongoDB**: Insere os dados processados em uma coleção MongoDB especificada.
*   **Resiliência**: Implementa lógicas de retentativa para conexões com MQTT e MongoDB.
*   **Configuração Flexível**: Utiliza variáveis de ambiente para configurar conexões e outros parâmetros.
*   **Suporte a MQTT v5**: Comunica-se com o broker usando o protocolo MQTT v5.
*   **Autenticação MQTT**: Suporta autenticação com nome de usuário e senha no broker MQTT.

## Pré-requisitos

*   Python 3.8+
*   Pip (gerenciador de pacotes Python)
*   Um broker MQTT (ex: Mosquitto, RabbitMQ com plugin MQTT) em execução e acessível.
*   Uma instância MongoDB em execução e acessível.

## Instalação de Dependências

Clone o repositório (se aplicável) e instale as dependências Python:

## Configuração

O projeto é configurado através das seguintes variáveis de ambiente:

*   `MQTT_BROKER_HOST`: Endereço do broker MQTT (padrão: `localhost`).
    *   *Nota para Docker*: Use o nome do serviço Docker (ex: `rabbitmq`) se o consumidor estiver rodando em um container na mesma rede Docker que o broker.
*   `MQTT_BROKER_PORT`: Porta do broker MQTT (padrão: `1883`).
*   `MQTT_TOPIC`: Tópico MQTT para subscrição (padrão: `weather/data`).
*   `MQTT_USERNAME`: Nome de usuário para autenticação no broker MQTT (padrão: `user`).
*   `MQTT_PASSWORD`: Senha para autenticação no broker MQTT (padrão: `password`).
*   `MONGO_URI`: URI de conexão do MongoDB (padrão: `mongodb://localhost:27017/`).
    *   *Nota para Docker*: Use o nome do serviço Docker (ex: `mongodb://mongodb:27017/`) se o consumidor estiver rodando em um container na mesma rede Docker que o MongoDB.
*   `MONGO_DATABASE`: Nome do banco de dados MongoDB (padrão: `trainstormdb`).
*   `MONGO_COLLECTION`: Nome da coleção MongoDB onde os eventos serão armazenados (padrão: `events`).

**Exemplo de configuração de ambiente (arquivo `.env` ou exportando no terminal):**

## Como Executar

### 1. Iniciar Broker MQTT e MongoDB

Certifique-se de que seu broker MQTT e sua instância MongoDB estejam em execução, acessíveis e configurados conforme as variáveis de ambiente.

### 2. Executar o Consumidor (`consumer.py`)

Navegue até o diretório `eventProcessor/src/` (ou onde o script `consumer.py` estiver localizado) e execute:

O consumidor tentará se conectar ao MongoDB e, em seguida, ao broker MQTT. Ele começará a escutar mensagens no tópico configurado e as inserirá no MongoDB. Logs de conexão, mensagens recebidas e operações de banco de dados serão exibidos no console.

## Estrutura dos Dados (Payload MQTT Esperado)

O consumidor espera receber mensagens no formato JSON. Por exemplo:

## Tecnologias Utilizadas

* Python 3.8+
* Paho MQTT (cliente MQTT para Python)
* PyMongo (cliente MongoDB para Python)
* MQTT v5
* MongoDB

## Pré-requisitos

- Python 3.8+ instalado
- Pip (gerenciador de pacotes Python)
- Broker MQTT (ex: RabbitMQ com plugin MQTT ou Mosquitto) em execução
- Instância MongoDB em execução

## Instalação de Dependências

No diretório raiz do projeto, execute:

```bash
pip install -r requirements.txt