import sys
sys.path.append("..")
sys.path.append(".")

from settings import Config
from database import Database,Device,Equipment
from logger import setup_logging
from sqlalchemy.orm import joinedload

SRC_DB = "base"
SRC_ADDR = "121.196.171.213"
SRC_PORT = 3306
SRC_USERNAME = "root"
SRC_PASSWORD = ""
PROJECT_ID = 5

if __name__ == "__main__":
    config = Config("config.yaml")
    mqtt_config = config.mqtt
    database_config = config.dababase
    addr = mqtt_config.addr
    port = mqtt_config.port
    username = mqtt_config.username
    password = mqtt_config.password

    logger = setup_logging()
    db_uri_target = f'mysql+pymysql://{database_config.username}:{database_config.password}@{database_config.addr}:{database_config.port}/{database_config.dbname}'
    database_tar = Database(db_uri_target,logger)

    db_uri_src = f'mysql+pymysql://{SRC_USERNAME}:{SRC_PASSWORD}@{SRC_ADDR}:{SRC_PORT}/{SRC_DB}'
    database_src = Database(db_uri_src,logger)

    eq_dict = {}
    with database_src.create_session() as session_src:
        with database_tar.create_session() as session_tar:
            equipments = (
                session_src.query(Equipment).all()
            )
            for equipment in equipments:
                print(equipment)
                new_id = database_tar.add_equipment(equipment.name,"",PROJECT_ID)
                eq_dict[equipment.id] = new_id

            devices = (
                session_src.query(Device).all()
            )
            for device in devices:
                if device.equipment_id is not None:
                    eq_id = eq_dict[device.equipment_id]
                else:
                    eq_id = None
                database_tar.add_device(device.name,eq_id)