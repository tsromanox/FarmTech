# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
from azure.iot.device import IoTHubDeviceClient
import certifi # Adicione esta importação

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


# define behavior for receiving a message
def message_handler(message):
    print("the data in the message received was ")
    print(message.data)
    print("custom properties are")
    print(message.custom_properties)


# set the message handler on the client
device_client.on_message_received = message_handler


# Wait for user to indicate they are done listening for messages
while True:
    selection = input("Press Q to quit\n")
    if selection == "Q" or selection == "q":
        print("Quitting...")
        break


# finally, shut down the client
device_client.shutdown()