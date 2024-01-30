from settings import Config
from database import Database
if __name__ == "__main__":
    config = Config("config.yaml")
    mqtt_config = config.mqtt
    database_config = config.dababase
    addr = mqtt_config.addr
    port = mqtt_config.port
    username = mqtt_config.username
    password = mqtt_config.password

    db_uri = f'mysql+pymysql://{database_config.username}:{database_config.password}@{database_config.addr}:{database_config.port}/{database_config.dbname}'
    database = Database(db_uri)

    with open("eq.csv","r") as f:
        lines = f.readlines()
        for line in lines:
            project_id,collector_id,meter_id,name = line.replace("\n","").split(",")
            eq_id = f"{project_id}-{meter_id}-{collector_id}"
            database.add_equipment(name,eq_id)