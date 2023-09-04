from machine import Pin, Timer
import time

button = Pin(0, Pin.IN, Pin.PULL_UP)
relay = Pin(1, Pin.OUT)
led = Pin(2, Pin.OUT)

time_running = 5 # 5*60
time_waiting = 1 # 20*60

timer_on = Timer()
timer_off = Timer()

def on():
    led.on()
    relay.on()
    
def off():
    led.off()
    relay.off()

def relay_timer_on(t):
    on()
    timer_off.init(period=(time_running*1000), mode=Timer.ONE_SHOT, callback=relay_timer_off)

def relay_timer_off(t):
    off()
    timer_on.init(period=(time_waiting * 1000), mode=Timer.ONE_SHOT, callback=relay_timer_on)

def toggle_relay(pin):
    val = pin.value()

    if val == 1:
        relay_timer_on(True)
    else:
        off()
        timer_on.deinit()
        timer_off.deinit()

    time.sleep(0.1)

button.irq(toggle_relay, Pin.IRQ_FALLING | Pin.IRQ_RISING)

toggle_relay(button)
