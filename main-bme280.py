import machine, time
import micropython, gc
import bme280
i2c=machine.I2C(scl=machine.Pin(22),sda=machine.Pin(21),speed=400000)
bme=bme280.BME280(i2c=i2c)
def bmevalues():
    t, p, h = bme.read_compensated_data()
    p = p // 256
    pi = p // 100
    pd = p - pi * 100
    hi = h // 1024
    hd = h * 100 // 1024 - hi * 100
    return "[{}] T={}C  ".format(time.strftime("%H:%M:%S",time.localtime()), t / 100) + "P={}.{:02d}hPa  ".format(pi, pd) + "H={}.{:02d}%".format(hi, hd)


while True:
    print(bmevalues())
    time.sleep(5)

