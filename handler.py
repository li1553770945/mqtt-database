from database import Database
import logging
import time
class MessageHandler:
    def __init__(self,database:Database,logger:logging.Logger) -> None:
        self.database = database
        self.last_update_time = time.time()
        self.logger = logger

    def on_message(self,client, userdata, msg):
        self.last_update_time = time.time()
        topic = msg.topic
        message = msg.payload.decode('utf-8')
        ids = topic.split("/")
        if len(ids) != 4:
            self.logger.warning(f"unknown topic:{topic}")
            return
        project_id,collector_id,meter_id = ids[1],ids[2],ids[3]
        print(project_id,collector_id,meter_id)
    
    