from settings import Config
from mqtt import MQTT

def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload.decode('utf-8')}' on topic '{msg.topic}' with QoS {str(msg.qos)}")

def main():
    config = Config("config.json")
    addr = config.addr
    port = config.port
    username = config.username
    password = config.password
    mqtt = MQTT(addr,port,username,password)
    mqtt.connect(on_message=on_message)

if __name__ == "__main__":
    main()