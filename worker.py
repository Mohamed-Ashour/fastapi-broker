import os
import json
import time
import paho.mqtt.client as mqtt
from app import crud, models, schemas, database

HOST = os.environ.get("MQTT_HOST", "localhost")
PORT = int(os.environ.get("MQTT_PORT", 1883))
TOPIC = os.environ.get("MQTT_TOPIC", "thndr-trading")

models.Base.metadata.create_all(bind=database.engine)


def on_connect(_client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    _client.subscribe(TOPIC)


def on_message(_client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    pld = json.loads(msg.payload)
    stock = schemas.Stock(**pld)
    db = database.SessionLocal()
    crud.add_stock(db, stock)
    crud.add_stock_log(db, stock)
    db.close()


# wait for connections
time.sleep(5)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(HOST, PORT)
client.loop_forever()
