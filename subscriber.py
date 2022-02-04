import paho.mqtt.client as mqtt
import time

client_topic = "ece180d/team6/test/brendan/client"
publisher_topic = "ece180d/team6/test/brendan/publisher"

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))

    client.subscribe(publisher_topic, qos = 1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected disconnect')
    else:
        print("Expected disconnect")

def on_message(client, userdata, message):
    print('Recieved mesage: "' + str(message.payload) + '" on topic "' + message.topic + '" with QoS ' + str(message.qos))
    startIndex = str(message.payload).find('\'')
    endIndex = str(message.payload).find('\'', startIndex + 1)
    count = int(str(message.payload)[startIndex + 1:endIndex]) + 1
    #time.sleep(3)
    client.publish(client_topic, str(count), qos=1)


client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect_async("test.mosquitto.org")

client.loop_start()

while True:
    pass

client.loop_stop()
client.disconnect()