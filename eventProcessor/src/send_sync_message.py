# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import time
import uuid
from azure.iot.device import IoTHubDeviceClient, Message
import certifi

# Configure o Python para usar os certificados CA do certifi
os.environ["SSL_CERT_FILE"] = certifi.where()

# The connection string for a device should never be stored in code. For the sake of simplicity we're using an environment variable here.
conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
if not conn_str:
    raise ValueError("The environment variable IOTHUB_DEVICE_CONNECTION_STRING is not defined.")
# The client object is used to interact with your Azure IoT hub.
device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

# Connect the client.
try:
    device_client.connect()
    print("Conectado ao Azure IoT Hub com sucesso!")
except Exception as e:
    print(f"Falha ao conectar ao Azure IoT Hub: {e}")
    exit()

# send 2 messages with 2 system properties & 1 custom property with a 1 second pause between each message
for i in range(1, 3):
    print("sending message #" + str(i))
    msg = Message("test wind speed " + str(i))
    msg.message_id = uuid.uuid4()
    msg.correlation_id = "correlation-1234"
    msg.custom_properties["tornado-warning"] = "yes"
    msg.content_encoding = "utf-8"
    msg.content_type = "application/json"
    device_client.send_message(msg)
    time.sleep(1)

# send 2 messages with only custom property with a 1 second pause between each message
for i in range(3, 5):
    print("sending message #" + str(i))
    msg = Message("test wind speed " + str(i))
    msg.custom_properties["tornado-warning"] = "yes"
    msg.content_encoding = "utf-8"
    msg.content_type = "application/json"
    device_client.send_message(msg)
    time.sleep(1)

# send 2 messages with only system properties with a 1 second pause between each message
for i in range(5, 7):
    print("sending message #" + str(i))
    msg = Message("test wind speed " + str(i))
    msg.message_id = uuid.uuid4()
    msg.correlation_id = "correlation-1234"
    msg.content_encoding = "utf-8"
    msg.content_type = "application/json"
    device_client.send_message(msg)
    time.sleep(1)

# send 2 messages with 1 system property and 1 custom property with a 1 second pause between each message
for i in range(7, 9):
    print("sending message #" + str(i))
    msg = Message("test wind speed " + str(i))
    msg.message_id = uuid.uuid4()
    msg.custom_properties["tornado-warning"] = "yes"
    msg.content_encoding = "utf-8"
    msg.content_type = "application/json"
    device_client.send_message(msg)
    time.sleep(1)

# send only string messages
for i in range(9, 11):
    print("sending message #" + str(i))
    device_client.send_message("test payload message " + str(i))
    time.sleep(1)


# finally, shut down the client
device_client.shutdown()