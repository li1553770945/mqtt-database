import random
from paho.mqtt import client as mqtt_client
import threading

class MQTT:
    def __init__(self,addr:str,port:int,username:str,password:str) -> None:
        self.addr = addr
        self.port = port
        self.username = username
        self.password = password
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'
        self.client = mqtt_client.Client(self.client_id)
        self.subscribe_list = list()
    
    def connect(self,on_message):
        semaphore = threading.Semaphore(0)
        print("test")
        def on_connect(client, userdata, flags, rc):
            print(rc)
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                raise AssertionError(f"Failed to connect, return code {rc}\n")
            semaphore.release()
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.connect(self.addr,self.port)
        self.client.loop_start()
        semaphore.acquire()

    def publish(self,topic,msg):
        result = self.client.publish(topic, msg)
        status = result[0]
        return status
    
    def subscribe(self,topic):
        self.client.subscribe(topic)
        self.subscribe_list.append(topic)
    
  
        