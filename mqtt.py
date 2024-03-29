import random
from paho.mqtt import client as mqtt_client
import threading

class MQTT:
    def __init__(self,addr:str,port:int,username:str,password:str,logger) -> None:
        self.addr = addr
        self.port = port
        self.username = username
        self.password = password
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'
        self.client = mqtt_client.Client(self.client_id)
        self.subscribe_list = list()
        self.logger = logger
    
    def connect(self,on_message):
        semaphore = threading.Semaphore(0)
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.logger.info("Connected to MQTT Broker!")
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
    
    def disconnect(self):
        self.client.disconnect()  # 发送断开连接的命令
        self.client.loop_stop()   # 停止网络循环
        self.client.loop_stop(True)  # 等待网络循环真正停止

    
  
        