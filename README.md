# Projeto FarmTech - Sistema Inteligente de Monitoramento Agrícola

# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

## **Projeto Base: Sistema de Irrigação Inteligente Simulado**

## FarmTech Solutions

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/company/inova-fusca">Anna Cecilia Moreira Cabral</a>
- <a href="https://www.linkedin.com/company/inova-fusca">Heitor Exposito de Sousa</a>
- <a href="https://www.linkedin.com/company/inova-fusca">Letícia Gomez Pinheiro</a> 
- <a href="https://www.linkedin.com/company/inova-fusca">Thiago Sabato Romano</a> 
- <a href="https://www.linkedin.com/company/inova-fusca">Vicenzo de Simone Montefusco</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/company/inova-fusca">Leonardo Ruiz Orabona</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/company/inova-fusca">Andre Godoi Chiovato</a>

Bem-vindo ao FarmTech! Esta é uma solução completa de IoT e Análise de Dados, projetada para monitorar, automatizar e otimizar operações agrícolas. O sistema coleta dados em tempo real do campo, os processa na nuvem e aplica modelos de Machine Learning para gerar insights valiosos.

## Visão Geral da Arquitetura

O FarmTech é composto por múltiplos módulos integrados, cada um responsável por uma etapa do fluxo de dados, automação e inteligência agrícola. A seguir, detalhamos cada componente e suas interações:

---

### 1. Dispositivo de Campo (`FarmTechIoT`)
- **Função:** Coleta dados ambientais (umidade, temperatura, luminosidade, etc.) e executa automações locais.
- **Hardware:** ESP32 (ou similar), sensores ambientais, atuadores (ex: relé para bomba d’água).
- **Firmware:** Desenvolvido em C++ (Arduino Framework).
- **Comunicação:** Envia dados em JSON via MQTT para o backend, utilizando Wi-Fi.
- **Automação Local:** Executa regras pré-configuradas para garantir operação mesmo offline.
- **Segurança:** Suporte a autenticação MQTT e criptografia (TLS, se configurado).

---

### 2. Broker de Mensagens (RabbitMQ/MQTT)
- **Função:** Centraliza a comunicação entre dispositivos e backend, desacoplando produtores e consumidores de eventos.
- **Tecnologia:** RabbitMQ com plugin MQTT.
- **Portas:** 
  - MQTT: 1883 (padrão)
  - AMQP: 5672
  - UI de Gerenciamento: 15672
- **Recursos:** Suporte a múltiplos tópicos, autenticação, plugins para extensibilidade.

---

### 3. Processador de Eventos (`eventProcessor`)
- **Função:** Consome mensagens MQTT, valida, enriquece e armazena os dados.
- **Tecnologia:** Python.
- **Principais Responsabilidades:**
  - Conexão robusta com o broker MQTT.
  - Decodificação e validação de mensagens JSON.
  - Enriquecimento dos dados com metadados (timestamp, ID do dispositivo, etc.).
  - Armazenamento eficiente no MongoDB.
  - Tratamento de falhas e reconexão automática.

---

### 4. Banco de Dados (MongoDB)
- **Função:** Armazena eventos históricos, permitindo consultas rápidas e flexíveis.
- **Tecnologia:** MongoDB (NoSQL, orientado a documentos).
- **Vantagens:** 
  - Escalabilidade horizontal.
  - Suporte a dados semi-estruturados.
  - Consultas flexíveis para análise e ML.

---

### 5. Análise e Machine Learning (`FarmTechML`)
- **Função:** Realiza análise exploratória, treinamento de modelos e inferência.
- **Tecnologia:** Python (Pandas, Scikit-learn, TensorFlow/PyTorch, Jupyter Notebooks).
- **Principais Atividades:**
  - Análise de padrões históricos.
  - Treinamento de modelos preditivos (ex: previsão de irrigação).
  - Detecção de anomalias em leituras de sensores.
  - Geração de relatórios e dashboards.
  - Exportação de modelos para uso em produção.

---

### 6. Recursos de Infraestrutura (`event-resource`)
- **Função:** Centraliza a definição e automação da infraestrutura e contratos de dados.
- **Tecnologias:** Docker, Docker Compose, Terraform, JSON Schema, OpenAPI.
- **Responsabilidades:**
  - Orquestração dos serviços (MongoDB, RabbitMQ, eventProcessor).
  - Infraestrutura como Código (IaC) para ambientes replicáveis.
  - Definição de contratos de dados (schemas) e APIs (OpenAPI).
  - Scripts de provisionamento e documentação.

---

### 7. Fluxo de Dados

1. **Coleta:** Dispositivos de campo capturam dados e publicam via MQTT.
2. **Ingestão:** Broker recebe e encaminha eventos ao processador.
3. **Processamento:** Dados são validados e enriquecidos pelo eventProcessor.
4. **Armazenamento:** Dados persistidos no MongoDB.
5. **Análise:** FarmTechML acessa dados históricos para gerar inteligência.
6. **Ação:** Insights podem ser usados para automação ou visualização em dashboards.

---

### 8. Segurança e Resiliência

- **Autenticação:** Usuários e dispositivos autenticados no broker.
- **Persistência:** Dados armazenados de forma segura e redundante.
- **Recuperação:** Serviços configurados para reinício automático e tolerância a falhas.
- **Monitoramento:** Logs e métricas disponíveis para acompanhamento do sistema.

---

Esta arquitetura modular permite fácil expansão, manutenção e integração com novos sensores, atuadores ou algoritmos de análise, tornando o FarmTech uma solução robusta para agricultura

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