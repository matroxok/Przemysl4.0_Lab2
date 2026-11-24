import datetime
import matplotlib


import matplotlib.pyplot as plt
import matplotlib.animation as animation
import paho.mqtt.client as mqtt



broker_address = "10.104.32.253"
broker_port = 1883
topic_sensor = "sensor/data"
topic_control = "control/led"

TEMP_THRESHOLD = 25.0

times = []
temps = []
hums = []

def on_message(client, userdata, message):
    global times, temps, hums
    payload = message.payload.decode("utf-8")
    try:
        temp, hum = map(float, payload.split(" "))
        now = datetime.datetime.now().strftime("%H:%M:%S")
        
        '''times.append(now)
        temps.append(temp)
        hums.append(hum)
        if len(times) > 15:
            times.pop(0)
            temps.pop(0)
            hums.pop(0)'''
            
        if temp > TEMP_THRESHOLD:
            client.publish(topic_control, "ON")
            print(f"[{now}] Temp: {temp:.2f}°C > {TEMP_THRESHOLD}°C -> Wysłano komendę: ON")
        else:
            client.publish(topic_control, "OFF")
            print(f"[{now}] Temp: {temp:.2f}°C <= {TEMP_THRESHOLD}°C -> Wysłano komendę: OFF")
            
    except ValueError:
        print("Błąd odebranego ładunku:", payload)

client = mqtt.Client()
client.on_message = on_message
client.connect(broker_address, broker_port)
client.subscribe(topic_sensor)

#start
client.loop_start()

#wykres
#fig, ax = plt.subplots()

"""def animate(i):
    ax.clear()
    if times:
        ax.plot(times, temps, label="Temperature (°C)", color="tab:blue", marker="o")
        ax.plot(times, hums, label="Humidity (%)", color="tab:orange", marker="o")
        ax.set_xlabel("Time")
        ax.set_ylabel("Value")
        ax.set_title("Wizualizacja parametrów w czasie rzeczywistym")
        ax.legend(loc="upper left")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

#refresh 5s
ani = animation.FuncAnimation(fig, animate, interval=5000)
plt.show()"""

client.loop_stop()
client.disconnect()