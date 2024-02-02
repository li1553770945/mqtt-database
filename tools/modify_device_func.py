import sys
sys.path.append("..")
sys.path.append(".")

from settings import Config
from database import Database,Device
from logger import setup_logging
from sqlalchemy.orm import joinedload

if __name__ == "__main__":
    config = Config("config.yaml")
    mqtt_config = config.mqtt
    database_config = config.dababase
    addr = mqtt_config.addr
    port = mqtt_config.port
    username = mqtt_config.username
    password = mqtt_config.password

    db_uri = f'mysql+pymysql://{database_config.username}:{database_config.password}@{database_config.addr}:{database_config.port}/{database_config.dbname}'
    database = Database(db_uri,setup_logging())

    with database.create_session() as session:

        devices = (
            session.query(Device).all()
        )
        for device in devices:
            print(device.name,device.function)
            if '累计' in device.name or '电能' in device.name:
                device.function = 'diff'
            else:
                device.function = 'avg'
            session.commit()

    