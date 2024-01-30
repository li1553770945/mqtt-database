# MQTT与数据库对接

## config样例

```yaml
mqtt:
  addr: xx
  port: 1883
  username: xx
  password: xx
  watchdog_timeout: 10 # 多长时间收不到数据自动重新连接，单位秒
database:
  addr: xx
  port: 3307
  username: root
  password: xx
  dbname: xx
```
