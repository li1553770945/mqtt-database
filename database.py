from sqlalchemy import create_engine, Column, Integer, String,ForeignKey,Double,DateTime,func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
import logging
from contextlib import contextmanager
import settings
Base = declarative_base()


class Equipment(Base):
    __tablename__ = 'tb_equipment'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    project_id = Column(Integer)
    mqtt_id = Column(String(255))
    create_time = Column(DateTime, default=func.now()) 
    devices = relationship("Device", back_populates="equipment")

    def __repr__(self):
        return f"<Equipment(name='{self.name})>"

class Device(Base):
    __tablename__ = 'tb_device'
    id = Column(Integer, primary_key=True)
    create_time = Column(DateTime, default=func.now()) 
    name = Column(String(255))
    function = Column(String(255))
    equipment_id = Column(Integer, ForeignKey('tb_equipment.id'))
    project_id = Column(Integer)
    equipment = relationship("Equipment", back_populates="devices")
    device_datas = relationship("DeviceData", back_populates="device")

    def __repr__(self):
        return f"<Device(name='{self.name})>"

class DeviceData(Base):
    __tablename__ = 'tb_device_data'
    id = Column(Integer, primary_key=True)
    create_time = Column(DateTime, default=func.now()) 
    device_id = Column(Integer, ForeignKey('tb_device.id'))
    data = Column(Double)
    device = relationship("Device", back_populates="device_datas")
    def __repr__(self):
        return f"<DeviceData(id='{self.id})>"
    
class Database:
    def __init__(self,config:settings.Config, uri:str,logger:logging.Logger):
        self.config = config
        self.logger = logger
        self.engine = create_engine(uri,pool_size=20,max_overflow=40,)
        self.Session = sessionmaker(bind=self.engine,expire_on_commit=False)
        Base.metadata.create_all(self.engine)
        self.logger.info("Successful connect to database!")

    @contextmanager
    def create_session(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as err:
            self.logger.error(f"Database error!:{err}")
            session.rollback()
            raise
        finally:
            session.close()

    def add_equipment(self, name, mqtt_id,project_id=None):
        with self.create_session() as session:
            new_equipment = Equipment(name=name,mqtt_id=mqtt_id,project_id=project_id)
            session.add(new_equipment)
        return new_equipment.id

    def get_equipment_by_mqtt_id(self,mqtt_id):
        with self.create_session() as session:
            equipments = session.query(Equipment).filter(Equipment.mqtt_id==mqtt_id).all()
            if len(equipments) == 0:
                return None
        return equipments[0]
    
    def add_device(self,name,equipment_id,project_id=None):
        project_id = self.config.mqtt.project_id
        with self.create_session() as session:
            new_device = Device(name=name,equipment_id=equipment_id,project_id=project_id)
            session.add(new_device)
        return new_device.id
    
    def get_device(self,equipment_id,name):
        with self.create_session() as session:
            devices = session.query(Device).filter(Device.equipment_id==equipment_id).filter(Device.name==name).all()
            if len(devices) == 0:
                return None
        return devices[0]
    
    def add_deivce_data(self,device_id,data,create_time=None):
        with self.create_session() as session:
            if create_time:
                new_device_data = DeviceData(device_id=device_id,data=data,create_time=create_time)
            else:
                new_device_data = DeviceData(device_id=device_id,data=data)
            session.add(new_device_data)
        return new_device_data.id



