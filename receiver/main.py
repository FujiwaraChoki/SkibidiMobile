from nrf24l01 import NRF24L01
from machine import SoftSPI, Pin
from time import sleep
import struct

# Define Pins for motor control
INPUT_1 = Pin(6, Pin.OUT)
INPUT_2 = Pin(7, Pin.OUT)
EN_A = Pin(8, Pin.OUT)

INPUT_3 = Pin(21, Pin.OUT)
INPUT_4 = Pin(22, Pin.OUT)
EN_B = Pin(27, Pin.OUT)

# Enable the motor drivers
EN_A.high()
EN_B.high()

# Define Pins for nRF24L01 module
CSN = Pin(14, mode=Pin.OUT, value=1)  # Chip Select Not
CE = Pin(17, mode=Pin.OUT, value=0)   # Chip Enable
LED = Pin(25, Pin.OUT)                # Onboard LED
PAYLOAD_SIZE = 20

# Define the communication pipes
SEND_PIPE = b"\xd2\xf0\xf0\xf0\xf0"
RECEIVE_PIPE = b"\xe1\xf0\xf0\xf0\xf0"

def setup():
    """
    Initialize the nRF24L01 module.
    
    Returns:
        NRF24L01: The initialized nRF24L01 object.
    """
    print("=> Initialising the nRF24L0+ Module")
    nrf = NRF24L01(SoftSPI(sck=Pin(2), mosi=Pin(3), miso=Pin(4)), CSN, CE, payload_size=PAYLOAD_SIZE)
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

def move_forward():
    """Move the robot forward."""
    INPUT_1.high()
    INPUT_2.low()
    INPUT_3.high()
    INPUT_4.low()

def move_backward():
    """Move the robot backward."""
    INPUT_1.low()
    INPUT_2.high()
    INPUT_3.low()
    INPUT_4.high()

def stop():
    """Stop the robot."""
    INPUT_1.low()
    INPUT_2.low()
    INPUT_3.low()
    INPUT_4.low()

while True:
    msg = ""
    # Check for Messages
    if nrf.any():
        package = nrf.recv()
        message = struct.unpack("s", package)
        msg = message[0].decode()
        flash_led(1)

        # Check for the new line character
        if (msg == "\n") and (len(msg_string) <= 20):
            print(f"[<=] Message: {msg_string}")
            if msg_string == "forward":
                move_forward()
            elif msg_string == "stop":
                stop()
            elif msg_string == "backward":
                move_backward()
            msg_string = ""
        else:
            if len(msg_string) <= 20:
                msg_string += msg
            else:
                msg_string = ""
