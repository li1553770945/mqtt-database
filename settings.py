import json
import yaml
class MQTTConfig:
    def __init__(self,config) -> None:
        self.addr = config['addr']
        self.port = config['port']
        self.username = config['username']
        self.password = config['password']
        self.watchdog_timeout = config['watchdog_timeout']  

class DatabaseConfig:
    def __init__(self,config) -> None:
        self.addr = config['addr']
        self.port = config['port']
        self.username = config['username']
        self.password = config['password']
        self.dbname = config['dbname']  

class Config:
    def __init__(self, config_file="config.yaml") -> None:
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
            self.mqtt = MQTTConfig(config['mqtt'])
            self.dababase = DatabaseConfig(config['database'])
            

    