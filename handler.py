from database import Database
import logging
import time
import json
class MessageHandler:
    def __init__(self,database:Database,logger:logging.Logger) -> None:
        self.database = database
        self.last_update_time = time.time()
        self.logger = logger

    def on_message(self,client, userdata, msg):
        self.last_update_time = time.time()
        topic = msg.topic
        message = msg.payload.decode('utf-8')
        self.logger.info(f"receive message from topic '{topic}':{message}")
        ids = topic.split("/")
        if len(ids) != 4:
            self.logger.warning(f"unknown topic:{topic}")
            return
        project_id,meter_id,collector_id, = ids[1],ids[2],ids[3]
        mqtt_id = f"{project_id}-{meter_id}-{collector_id}"
        equipment = self.database.get_equipment_by_mqtt_id(mqtt_id)
        if equipment is None:
            self.logger.warning(f"Unknown equipment mqttid:{mqtt_id}")
            return
        try:
            data = json.loads(message)
        except Exception as err:
            self.logger.warning(f"message decode to json error! {err}")
            return
        
        for device_name, value in data.items():
            if device_name[0] == "_":
                continue
            device_full_name = equipment.name +"-" +device_name
            device = self.database.get_device(equipment_id=equipment.id,name=device_full_name)
            if device is None:
                self.logger.warning(f"Can't find device for equitment:{equipment.name},name:{device_name},add it")
                device_id = self.database.add_device(device_full_name,equipment_id=equipment.id)
            else:
                device_id = device.id

            self.database.add_deivce_data(device_id=device_id,data=float(value))
            self.logger.info(f"Successful add data,equitment:{equipment.name},device:{device_name}")
    
    