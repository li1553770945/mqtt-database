

import sys
sys.path.append("..")
sys.path.append(".")
from settings import Config
from database import Database
from logger import setup_logging
from datetime import datetime,timedelta
cols= ["采集时刻","总用气量（m3）","燃气碳排放因子kgCO2/kWh","建筑总用电量kWh","空调系统总电量","照明插座用电量","动力系统用电量","特殊用电量","光伏发电量kWh","原电网碳排放因子kgCO2/kWh","现电网碳排放因子kgCO2/kWh","电力碳排放量（kgCO2）","空调系统碳排放量（kgCO2）","照明插座排放量（kgCO2）","动力系统碳排放量（kgCO2）","特殊用电碳排放量（kgCO2）","用气碳排放量kgCO2","光伏发电减碳量","节能改造减碳量"]


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
    # for col in cols:
    #     database.add_device(col,None)

    with open("tools/data.csv","r") as f:
        lines = f.readlines()
        for d in range(1,len(lines)-1):
            data = lines[d].replace("\n","").split(",")
            next_data = lines[d+1].replace("\n","").split(",")
            if data[0] == "":
                    continue
            start_id = 1363
            start = datetime.strptime(data[0],"%Y/%m/%d")
            end = start + timedelta(days=1)
            current = start
            print(d,":",current)
            for i in range(1,len(data)):
                

                minute5 = 0
                while current < end:
                    current += timedelta(minutes=5)
                    interval = ( float(next_data[i]) - float(data[i]) )/288
                    database.add_deivce_data(start_id+i,float(data[i])+interval*minute5,current)
                    minute5+=1