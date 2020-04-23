import time
import unidecode
import spidev
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24

battery_levels = [0]*num_devices


def init_radio():
    pipes=[[0xe8,0xe8,0xf0,0xf0,0xe1],[0xf0,0xf0,0xf0,0xf0,0xe1]]
    GPIO.setmode(GPIO.BCM)
    radio = NRF24(GPIO,spidev.SpiDev())
    radio.begin(0,17)
    radio.setDataRate(NRF24.BR_2MBPS)
    radio.setPALevel(NRF24.PA_MAX)
    radio.setAutoAck(True)
    radio.enableDynamicPayloads()
    radio.openWritingPipe(pipes[0])
    radio.openReadingPipe(1, pipes[1])

def setup_lock(lock_name):
    radio.setChannel(0x01)
    init_radio()
    radio_msg = list(lock_name)
    while len(radio_msg)<32:
        radio_msg.append(0)
    radio.write(radio_msg)
    start =time.time()
    while not radio.available():
        if(time.time()-start > 5):
            return false
        else:
            return true

def unlock_function(lock):
    wakeup_locks()
    radio.setChannel(0x76)
    init_radio()
    radio_msg = list(lock)
    while len(radio_msg)<32:
        radio_msg.append(0)
    radio.write(radio_msg)
    start = time.time()
    while not radio.available(0):
        time.sleep(1/100)
        if(time.time() - start > 2):
            return false
        else:
            return true
    radio.startListening();
    receivedMessage=[0]*32
    if(radio.available())
    {
        battery_level_dev = radio.read(receivedMessage, sizeof(receivedMessage))
        battery_levels[lock]=battery_level_dev
        if(battery_level_dev < 3.2):
            GPIO.setup(21, GPIO.out)
            GPIO.output(21, GPIO.HIGH)
            Lock_b=Lock.query.filter_by(lock_name = lock)
            Lock_b.battery = "Low"
    }


def wakeup_locks():
    GPIO.setup(23, GPIO.out)
    GPIO.setup(24, GPIO.out)
    GPIO.output(23, GPIO.HIGH)
    GPIO.output(24, GPIO.HIGH)

def sleep_locks():
    GPIO.output(23, GPIO.LOW)
    GPIO.output(24, GPIO.LOW)
