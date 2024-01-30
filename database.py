from sqlalchemy import create_engine, Column, Integer, String,ForeignKey,Double
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship

Base = declarative_base()


class Equipment(Base):
    __tablename__ = 'tb_equipment'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    mqtt_id = Column(String(255))
    devices = relationship("Device", back_populates="equipment")

    def __repr__(self):
        return f"<Equipment(name='{self.name})>"

class Device(Base):
    __tablename__ = 'tb_device'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    equipment_id = Column(Integer, ForeignKey('tb_equipment.id'))
    equipment = relationship("Equipment", back_populates="devices")
    device_datas = relationship("DeviceData", back_populates="device")

    def __repr__(self):
        return f"<Device(name='{self.name})>"

class DeviceData(Base):
    __tablename__ = 'tb_device_data'
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('tb_device.id'))
    data = Column(Double)
    device = relationship("Device", back_populates="device_datas")
    def __repr__(self):
        return f"<DeviceData(id='{self.id})>"
    
class Database:
    def __init__(self, uri):
        self.engine = create_engine(uri)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def create_session(self):
        return self.Session()

    def add_equipment(self, name, mqtt_id):
        session = self.create_session()
        new_equipment = Equipment(name=name,mqtt_id=mqtt_id)
        session.add(new_equipment)
        session.commit()



