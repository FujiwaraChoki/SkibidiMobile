import struct

from time import sleep
from nrf24l01 import NRF24L01
from machine import SoftSPI, Pin

# Initialize the pins for the nRF24L01 module
CSN = Pin(14, mode=Pin.OUT, value=1)  # Chip Select Not
CE = Pin(17, mode=Pin.OUT, value=0)   # Chip Enable
LED = Pin(25, Pin.OUT)                # Onboard LED
PAYLOAD_SIZE = 20
IR_SENSOR = Pin(22, Pin.IN, Pin.PULL_UP)  # Sensor input pin

# Define the communication pipes
SEND_PIPE = b"\xe1\xf0\xf0\xf0\xf0"
RECEIVE_PIPE = b"\xd2\xf0\xf0\xf0\xf0"


def setup():
    """
    Initialize the nRF24L01 module.
    
    Returns:
        NRF24L01: The initialized nRF24L01 object.
    """
    print("=> Initialising the nRF24L0+ Module")
    nrf = NRF24L01(SoftSPI(sck=Pin(2), mosi=Pin(3), miso=Pin(4)), CSN, CE, PAYLOAD_SIZE=PAYLOAD_SIZE)
    nrf.open_tx_pipe(SEND_PIPE)
    nrf.open_rx_pipe(1, RECEIVE_PIPE)
    nrf.start_listening()
    return nrf

def flash_led(times: int = None):
    """
    Flash the built-in LED the specified number of times.
    
    Parameters:
        times (int): Number of times to flash the LED.
    """
    for _ in range(times):
        LED.value(1)
        sleep(0.01)
        LED.value(0)
        sleep(0.01)

def send(nrf, msg):
    """
    Send a message using the nRF24L01 module.
    
    Parameters:
        nrf (NRF24L01): The initialized nRF24L01 object.
        msg (str): The message to send.
    """
    print(f"=> Sending message: {msg}")
    nrf.stop_listening()
    for n in range(len(msg)):
        try:
            encoded_string = msg[n].encode()
            byte_array = bytearray(encoded_string)
            buf = struct.pack("s", byte_array)
            nrf.send(buf)
            flash_led(1)
        except OSError:
            print("=> Error: Message not sent")
    nrf.send(b"\n")
    nrf.start_listening()

# Main code loop
flash_led(1)
nrf = setup()
nrf.start_listening()
msg_string = ""

while True:
    msg = ""
    if IR_SENSOR.value() == 0:
        send(nrf, "forward")
        sleep(1)
    else:
        print("=> Waiting")
        send(nrf, "stop")
        sleep(1)
