import time
import unidecode
import spidev
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24


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
