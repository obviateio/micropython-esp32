# Originally from:
# https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/blob/master/MicroPython_BUILD/components/micropython/esp32/modules_examples/bme280.py
import machine, _thread, time
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

def bmerun(interval=10):
    _thread.allowsuspend(True)
    sendmsg = True
    send_time = time.time() + interval
    while True:
        while time.time() < send_time:
            notif = _thread.getnotification()
            if notif == 10002:
                _thread.sendmsg(_thread.getReplID(), bmevalues())
            elif notif == 10004:
                sendmsg = False
            elif notif == 10006:
                sendmsg = True
            elif (notif <= 3600) and (notif >= 10):
                interval = notif
                send_time = time.time() + interval
                _thread.sendmsg(_thread.getReplID(), "Interval set to {} seconds".format(interval))
                
            time.sleep_ms(100)
        send_time = send_time + interval
        if sendmsg:
            _thread.sendmsg(_thread.getReplID(), bmevalues())

_thread.stack_size(3*1024)
bmeth=_thread.start_new_thread("BME280", bmerun, (10,))
