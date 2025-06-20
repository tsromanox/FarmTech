# Event Consumer

This project is designed to consume events from a RabbitMQ MQTT topic and insert them into a MongoDB database. It consists of a Python application that connects to RabbitMQ, subscribes to a specified topic, and processes incoming messages.

## Project Structure

```
event-consumer
├── src
│   ├── consumer.py       # Main logic for consuming events
│   └── config.py         # Configuration settings
├── requirements.txt       # Python dependencies
├── docker-compose.yml      # Docker services configuration
└── README.md              # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd event-consumer
   ```

2. **Build and run the services using Docker Compose:**
   ```bash
   docker-compose up -d
   ```

   This command will start the MongoDB and RabbitMQ services with MQTT enabled.

3. **Install Python dependencies:**
   You can install the required Python packages by running:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

- The consumer will automatically connect to the RabbitMQ server and start listening for messages on the specified MQTT topic.
- Incoming messages will be processed and inserted into the MongoDB database.

## Configuration

- Modify the `src/config.py` file to update the RabbitMQ connection parameters and MongoDB connection string as needed.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.