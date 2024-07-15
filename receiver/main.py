import time
import struct
from nrf24l01 import NRF24L01
from machine import Pin, SoftSPI

# Define Pins
INPUT_1 = Pin(6, Pin.OUT)
INPUT_2 = Pin(7, Pin.OUT)
EN_A = Pin(8, Pin.OUT)

INPUT_3 = Pin(21, Pin.OUT)
INPUT_4 = Pin(22, Pin.OUT)
EN_B = Pin(27, Pin.OUT)

EN_A.high()
EN_B.high()

CSN = Pin(14, Pin.OUT, value=1)
CE = Pin(17, Pin.OUT, value=0)
LED = Pin("LED", Pin.OUT)

PAYLOAD_SIZE = 32

SEND_PIPE = b"\xe1\xf0\xf0\xf0\xf0"
RECV_PIPE = b"\xd2\xf0\xf0\xf0\xf0"

# Setup the nRF24L01 Radio
def setup_radio():
    radio = NRF24L01(SoftSPI(sck=Pin(2), mosi=Pin(3), miso=Pin(4)), CSN, CE, payload_size=PAYLOAD_SIZE)
    radio.open_tx_pipe(SEND_PIPE)
    radio.open_rx_pipe(1, RECV_PIPE)
    radio.start_listening()
    return radio

# Function to move motors forward
def move_forward():
    INPUT_1.high()
    INPUT_2.low()
    INPUT_3.high()
    INPUT_4.low()

# Function to move motors backward
def move_backward():
    INPUT_1.low()
    INPUT_2.high()
    INPUT_3.low()
    INPUT_4.high()

# Function to stop motors
def stop():
    INPUT_1.low()
    INPUT_2.low()
    INPUT_3.low()
    INPUT_4.low()

# Function to flash the LED
def flash_led(n):
    for _ in range(n):
        LED.high()
        time.sleep(0.1)
        LED.low()
        time.sleep(0.1)

# Main Loop
def main():
    global msg_string

    nrf = setup_radio()
    msg_string = ""

    while True:
        if nrf.any():
            flash_led(3)
            package = nrf.recv()
            message = struct.unpack("s", package)
            msg = message[0].decode()

            print("[<=] Received: ", msg)

            if (msg == "\n") and (len(msg_string) > 0):
                print("[<=] Message: ", msg_string)
                if msg_string == "f":
                    move_forward()
                elif msg_string == "b":
                    move_backward()
                else:
                    stop()

                msg_string = ""
            else:
                if len(msg_string) < PAYLOAD_SIZE:
                    msg_string += msg
                else:
                    msg_string = ""

        time.sleep(1)

if __name__ == "__main__":
    main()
