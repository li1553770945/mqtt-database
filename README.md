# MQTT与数据库对接

## config样例

```yaml
mqtt:
  addr: xx
  port: 1883
  username: xx
  password: xx
  watchdog_timeout: 10 # 多长时间收不到数据自动重新连接，单位秒
  device_id: 2
database:
  addr: xx
  port: 3307
  username: root
  password: xx
  dbname: xx
```

## tools说明

+ upload_equipment: 手动添加equipment
+ add_device_and_data: 手动添加一些设备和数据
+ copy_from_other_database.py: 从其他平台复制equipment和device，且能保持其对应关系
+ rename_device: 批量重命名点位
