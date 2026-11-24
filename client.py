import paho.mqtt.client as mqtt

broker_address = "10.104.32.253"
broker_port = 1883
topic = "sensor/data"

def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    temp, hum = map(float, payload.split(" "))
    print(f"Odebrano z MQTT  Temperatura: {temp:.2f}°C | Wilgotność: {hum:.2f}%")

client = mqtt.Client()
client.on_message = on_message

client.connect(broker_address, broker_port)
client.subscribe(topic)

print(f"Subskrypcja tematu '{topic}' na brokerze {broker_address}:{broker_port}...")
client.loop_forever()