# Projeto FarmTech - Sistema Inteligente de Monitoramento Agrícola

Bem-vindo ao FarmTech! Esta é uma solução completa de IoT e Análise de Dados, projetada para monitorar, automatizar e otimizar operações agrícolas. O sistema coleta dados em tempo real do campo, os processa na nuvem e aplica modelos de Machine Learning para gerar insights valiosos.

## Visão Geral da Arquitetura

A arquitetura é composta por um dispositivo de campo (`FarmTechIOT`), um pipeline de processamento de eventos (`eventProcessor`), um banco de dados, um componente de análise (`FarmTechML`) e recursos de infraestrutura (`event-resource`).

```mermaid
flowchart TD
    subgraph CAMPO [Dispositivo de Campo]
        FT_IOT[ESP32<br/>FarmTechIOT]
    end

    subgraph NUVEM [Backend / Cloud]
        MQTT_BROKER[Broker MQTT<br/>(RabbitMQ/MQTT)]
        EVENT_PROC[eventProcessor<br/>(Python)]
        MONGODB[(MongoDB)]
        ML[FarmTechML<br/>(Python ML)]
        INSIGHTS((Insights & Previsões))
    end

    subgraph INFRA [Infraestrutura & CI/CD]
        EVENT_RESOURCE[event-resource<br/>(IaC, Docker, Schemas)]
    end

    FT_IOT -- "1. Publica dados (JSON via MQTT)" --> MQTT_BROKER
    MQTT_BROKER -- "2. Encaminha dados" --> EVENT_PROC
    EVENT_PROC -- "3. Armazena dados brutos" --> MONGODB
    ML -- "4. Lê dados históricos" --> MONGODB
    ML -- "5. Gera insights/modelos" --> INSIGHTS

    EVENT_RESOURCE -- "Provisiona/Define" --> MQTT_BROKER
    EVENT_RESOURCE -- "Provisiona/Define" --> EVENT_PROC
    EVENT_RESOURCE -- "Provisiona/Define" --> MONGODB
    EVENT_RESOURCE -- "Provisiona/Define" --> ML

    style FT_IOT fill:#b6e7a6,stroke:#333,stroke-width:2px
    style EVENT_PROC fill:#a6d8f7,stroke:#333,stroke-width:2px
    style ML fill:#ffd59a,stroke:#333,stroke-width:2px
    style EVENT_RESOURCE fill:#e0e0e0,stroke:#333,stroke-width:2px
```

---

## Estrutura de Diretórios

O projeto está organizado em quatro diretórios principais, cada um com uma responsabilidade clara:

### 1. `/FarmTechIOT` - Firmware do Dispositivo de Campo

Este diretório contém o código-fonte para o microcontrolador (ESP32) que opera no campo. É a ponta do sistema que interage com o ambiente físico.

-   **Propósito:** Coletar dados ambientais e executar automações locais.
-   **Tecnologia:** C++ (Arduino Framework).
-   **Responsabilidades:**
    1.  **Coleta de Dados:** Realiza leituras contínuas de sensores (ex: umidade, temperatura).
    2.  **Automação Local:** Controla atuadores (ex: bomba d'água) com base em regras pré-definidas, garantindo a operação mesmo sem conectividade.
    3.  **Comunicação Segura:** Publica os dados coletados em formato JSON para um broker MQTT na nuvem, utilizando o protocolo Wi-Fi.

### 2. `/eventProcessor` - Processador de Eventos

Este é o serviço de backend responsável por receber e processar os dados enviados pelos dispositivos `FarmTechIOT`.

-   **Propósito:** Servir como o pipeline de ingestão, validação e armazenamento de dados.
-   **Tecnologia:** Python.
-   **Responsabilidades:**
    1.  **Ingestão de Dados:** Atua como um consumidor MQTT, "escutando" os tópicos onde os dispositivos publicam suas leituras.
    2.  **Processamento e Validação:** Decodifica as mensagens JSON, valida a integridade dos dados e pode enriquecê-los com informações adicionais (ex: metadados do dispositivo).
    3.  **Armazenamento:** Insere os dados processados em um banco de dados (MongoDB), criando um repositório de dados históricos para análise.
    4.  **Resiliência:** Implementa lógicas de reconexão para garantir a robustez contra falhas no broker ou no banco de dados.

### 3. `/FarmTechML` - Análise e Machine Learning

Este diretório abriga os componentes de ciência de dados do projeto. Ele utiliza os dados históricos para extrair conhecimento e criar modelos preditivos.

-   **Propósito:** Transformar dados brutos em inteligência acionável.
-   **Tecnologia:** Python (com bibliotecas como Pandas, Scikit-learn, TensorFlow/PyTorch).
-   **Responsabilidades:**
    1.  **Análise Exploratória:** Contém notebooks (ex: Jupyter) para explorar os dados armazenados no MongoDB e identificar padrões.
    2.  **Treinamento de Modelos:** Scripts para treinar, avaliar e salvar modelos de Machine Learning. Exemplos de modelos incluem:
        -   **Previsão:** Estimar a necessidade de água futura com base em tendências de umidade e previsões do tempo.
        -   **Detecção de Anomalias:** Identificar leituras de sensores anormais que possam indicar falha de equipamento ou estresse da planta.
    3.  **Inferência:** Scripts que aplicam os modelos treinados para gerar previsões ou alertas, que podem ser usados para otimizar a irrigação ou notificar os operadores.

### 4. `/event-resource` - Recursos de Infraestrutura e API

Este diretório centraliza a configuração e a definição dos recursos da plataforma, promovendo as práticas de Infraestrutura como Código (IaC) e garantindo a consistência do ambiente.

-   **Propósito:** Definir, versionar e automatizar o provisionamento da infraestrutura de backend.
-   **Tecnologias:** Docker, Docker Compose, Terraform, JSON Schema, OpenAPI.
-   **Responsabilidades:**
    1.  **Orquestração de Serviços (`docker-compose.yml`):** Define como os serviços de backend (MQTT Broker, `eventProcessor`, MongoDB, etc.) são executados e conectados em um ambiente de desenvolvimento local.
    2.  **Infraestrutura como Código (IaC):** Pode conter scripts (ex: Terraform, Ansible) para provisionar a infraestrutura necessária em um provedor de nuvem (AWS, Azure, GCP).
    3.  **Definição de Contratos (`schemas/`):** Armazena esquemas (ex: JSON Schema) que definem a estrutura exata dos eventos MQTT. Isso garante que o `FarmTechIOT` e o `eventProcessor` "falem a mesma língua".
    4.  **Definição de APIs (`api/`):** Se o sistema expuser uma API REST para um dashboard, por exemplo, os arquivos de especificação (ex: OpenAPI/Swagger) estariam aqui.

---

## Fluxo de Dados e Inteligência

1.  O **`FarmTechIOT`** envia dados de sensores para o **Broker MQTT**.
2.  O **`eventProcessor`** consome, valida e armazena esses dados no **MongoDB**.
3.  Periodicamente, ou sob demanda, o **`FarmTechML`** lê os dados históricos do MongoDB para treinar modelos ou executar análises.
4.  Os insights e previsões gerados pelo `FarmTechML` podem ser usados para ajustar as regras no `FarmTechIOT` ou exibidos em um painel de controle.
5.  Todo o ambiente de backend é definido e pode ser replicado usando os arquivos no diretório **`event-resource`**.