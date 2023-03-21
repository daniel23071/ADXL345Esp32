import machine
import network
import time
from mqtt import MQTTClient
from micropython import const

# Configuración de la conexión WiFi
ssid = 'ASCALAFO'
password = '12345678'
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while not station.isconnected():
    pass

USERNAME = const('AQcNOjEBExEUGyoUCBwiPDk')
CLIENTID = const('AQcNOjEBExEUGyoUCBwiPDk')
PASS = const('LXmlIhN/XbGAbWweg6e6PFhD')
SERVER=const('mqtt3.thingspeak.com')
CHANNEL=const('2073528')
client = MQTTClient(client_id=CLIENTID, server=SERVER,user=CLIENTID,password=PASS )
#client.set_callback(sub_cb) 
#client.connect()
#client.subscribe(topic='channels/'+CHANNEL+'/subscribe/fields/field2')


# Configuración del ADXL345
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
addr = 0x53
i2c.writeto(addr, bytearray([0x31, 0x08]))


# Función para leer los datos de aceleración
def read_acceleration():
    data = i2c.readfrom_mem(addr, 0x32, 6)
    x = (data[1] << 8) | data[0]
    y = (data[3] << 8) | data[2]
    z = (data[5] << 8) | data[4]
    if x > 32767:
        x -= 65536
    if y > 32767:
        y -= 65536
    if z > 32767:
        z -= 65536
    return x, y, z


# Función para enviar los datos de aceleración a ThingSpeak
def send_data(x, y, z):
    payload = 'field1=' + str(x) + '&field2=' + str(y) + '&field3=' + str(z)
    client.connect()
    client.publish(topic="channels/"+CHANNEL+"/publish", msg=payload)  
    #client.publish('channels/' + USERNAME + '/publish/' + PASS + '/channel/' + CHANNEL + '/', payload)
    
    client.disconnect()

# Bucle principal para leer y enviar los datos de aceleración
while True:
    x, y, z = read_acceleration()
    send_data(x, y, z)
    time.sleep(30) # Espera de 30 segundos antes de volver a enviar los datos

