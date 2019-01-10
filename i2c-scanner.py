import machine
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
for i in i2c.scan():
    print(hex(i))
