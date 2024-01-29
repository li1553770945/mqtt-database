import json

class Config:
    def __init__(self,config_file="config.json") -> None:
        with open(config_file,"r") as f:
            config = json.load(f)
            self.addr = config['addr']
            self.port = config['port']
            self.username = config['username']
            self.password = config['password']
    