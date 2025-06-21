# event-resource — Infraestrutura do Backend FarmTech

Este diretório define e provisiona a infraestrutura essencial para o backend do FarmTech, utilizando Docker Compose para orquestrar MongoDB e RabbitMQ (com suporte MQTT).

---

## 📁 Estrutura do Diretório

```
event-resource/
├── docker-compose.yml         # Orquestração dos serviços MongoDB e RabbitMQ/MQTT
├── requirements.txt           # Dependências Python para integração com os serviços
├── mongodb/
│   └── data/                  # Persistência de dados do MongoDB (volume local)
├── rabbitmq/
│   └── enabled_plugins        # Plugins habilitados no RabbitMQ (inclui MQTT)
└── README.md                  # Este arquivo
```

---

## 🚀 Serviços Provisionados

- **MongoDB**
  - Banco de dados NoSQL para armazenamento dos eventos coletados.
  - Porta padrão: `27017`
  - Dados persistidos em `mongodb/data/`.

- **RabbitMQ (com MQTT)**
  - Broker de mensagens com suporte ao protocolo MQTT, permitindo integração com dispositivos IoT e aplicações Python.
  - Porta AMQP: `5672`
  - Porta MQTT: `1883`
  - Interface de gerenciamento: [http://localhost:15672](http://localhost:15672)
    - Usuário: `user`
    - Senha: `password`
  - Plugins habilitados: MQTT, Management (ver [`rabbitmq/enabled_plugins`](rabbitmq/enabled_plugins))

---

## ⚙️ Como Subir o Ambiente

1. **Suba os serviços com Docker Compose:**
   ```sh
   docker-compose up -d
   ```
   Isso iniciará MongoDB e RabbitMQ com MQTT habilitado.

2. **Verifique os containers:**
   ```sh
   docker ps
   ```

3. **Acesse o RabbitMQ Management UI:**  
   [http://localhost:15672](http://localhost:15672)  
   Usuário: `user` &nbsp;&nbsp; Senha: `password`

---

## 🐍 Dependências Python

Se for rodar consumidores/produtores Python fora do container, instale as dependências:
```sh
pip install -r requirements.txt
```
- **aio-pika**: Cliente assíncrono para RabbitMQ (AMQP)
- **pymongo**: Cliente MongoDB para Python
- **dnspython**: Suporte a DNS para conexões MongoDB

---

## 📝 Observações e Customizações

- Para alterar configurações (usuário, senha, nomes de volumes), edite o arquivo [`docker-compose.yml`](docker-compose.yml).
- O diretório `mongodb/data/` garante persistência dos dados mesmo após reiniciar os containers.
- O arquivo [`rabbitmq/enabled_plugins`](rabbitmq/enabled_plugins) garante que o plugin MQTT esteja ativo.
- Caso queira usar volumes nomeados do Docker, descomente as linhas correspondentes em `docker-compose.yml`.

---

## 🛠️ Troubleshooting

- **Portas em uso:** Certifique-se de que as portas `27017`, `5672`, `15672` e `1883` estejam livres.
- **Persistência:** Se quiser limpar os dados do MongoDB, apague o conteúdo da pasta `mongodb/data/` com os containers parados.
- **Logs:** Use `docker-compose logs -f` para acompanhar os logs dos serviços.

---

## 📄 Licença

MIT