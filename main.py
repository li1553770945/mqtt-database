from settings import Config
from mqtt import MQTT
import time
from logger import setup_logging


last_update_time = time.time()
logger = setup_logging()

def on_message(client, userdata, msg):
    global last_update_time
    logger.info(f"Received message '{msg.payload.decode('utf-8')}' on topic '{msg.topic}' with QoS {str(msg.qos)}")
    last_update_time = time.time()


def main():
    global last_update_time
    while True:
        config = Config("config.yaml")
        addr = config.addr
        port = config.port
        username = config.username
        password = config.password
        mqtt = MQTT(addr,port,username,password,logger)
        mqtt.connect(on_message=on_message)
        mqtt.subscribe("data/#")
        while True:
            time.sleep(config.watchdog_timeout/2)
            if time.time() - last_update_time > config.watchdog_timeout:
                logger.warning("watch dog timeout! restart!")
                mqtt.disconnect()
                last_update_time = time.time()
                break
        


if __name__ == "__main__":
    main()