from settings import Config
from mqtt import MQTT
import time
from logger import setup_logging
from handler import MessageHandler
from database import Database
def main():
    logger = setup_logging()
    config = Config("config.yaml")
    mqtt_config = config.mqtt
    database_config = config.dababase
    addr = mqtt_config.addr
    port = mqtt_config.port
    username = mqtt_config.username
    password = mqtt_config.password

    db_uri = f'mysql+pymysql://{database_config.username}:{database_config.password}@{database_config.addr}:{database_config.port}/{database_config.dbname}'
    database = Database(config,db_uri,logger)
    handler = MessageHandler(database,logger)

    while True:
        mqtt = MQTT(addr,port,username,password,logger)
        mqtt.connect(on_message=handler.on_message)
        mqtt.subscribe("data/#")
        while True:
            time.sleep(mqtt_config.watchdog_timeout/2)
            if time.time() - handler.last_update_time > mqtt_config.watchdog_timeout:
                logger.warning("watch dog timeout! restart!")
                mqtt.disconnect()
                handler.last_update_time = time.time()
                break
        


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as err:
            print("System Error! Restart System!",err)