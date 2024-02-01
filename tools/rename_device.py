import sys
sys.path.append("..")
sys.path.append(".")

from settings import Config
from database import Database,Device,Equipment
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

    logger = setup_logging()


    db_uri = f'mysql+pymysql://{database_config.username}:{database_config.password}@{database_config.addr}:{database_config.port}/{database_config.dbname}'

    database = Database(db_uri,logger)

    with database.create_session() as session:
       
            devices = (
                session.query(Device).filter(Device.id<=2186).filter(Device.id>=2075).all()
            )
            print(devices)
            for device in devices:
                equpment = session.query(Equipment).filter(Equipment.id==device.equipment_id).first()
                if equpment is not None:
                    device.name = equpment.name + "-" + device.name
                    session.commit()