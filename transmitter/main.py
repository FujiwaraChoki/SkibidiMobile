import time
import struct

from machine import Pin, SoftSPI
from nrf24l01 import NRF24L01

# Define Pins
CSN = Pin(14, Pin.OUT, value=1)
CE = Pin(17, Pin.OUT, value=0)
LED = Pin("LED", Pin.OUT)
PAYLOAD_SIZE = 20

SEND_PIPE = b"\xe1\xf0\xf0\xf0\xf0"
RECV_PIPE = b"\xd2\xf0\xf0\xf0\xf0"

# Function to flash the LED
def flash_led(n):
    for _ in range(n):
        LED.value(1)
        time.sleep(0.1)
        LED.value(0)
        time.sleep(0.1)

def send(nrf, msg):
    print("sending message.", msg)
    nrf.stop_listening()
    for n in range(len(msg)):
        try:
            encoded_string = msg[n].encode()
            byte_array = bytearray(encoded_string)
            buf = struct.pack("s", byte_array)
            nrf.send(buf)
            # print(role,"message",msg[n],"sent")
            flash_led(1)
        except OSError:
            print("Message not sent")
    nrf.send("\n")
    nrf.start_listening()

# Setup the nRF24L01 Radio
def setup_radio():
    radio = NRF24L01(SoftSPI(sck=Pin(2), mosi=Pin(3), miso=Pin(4)), CSN, CE, payload_size=PAYLOAD_SIZE)
    radio.open_tx_pipe(SEND_PIPE)
    radio.open_rx_pipe(1, RECV_PIPE)
    radio.start_listening()
    return radio

# Main Loop
def main():
    radio = setup_radio()
    while True:
        send(radio, "forward")

if __name__ == "__main__":
    main()
