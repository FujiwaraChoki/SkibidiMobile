# SkibidiMobile

The SkibdiMobile is a car-like thing that can be driven based on Analog Input from an Infrared Sensor.

It uses two DC motors in the back, and one motor-less wheel in the front.

3mf files are located in the [3d](3d) directory.

I used Shapr3D to design the parts, since it's way easier to use compared to other software like Blender or Fusion360.

To make both transmitter and receiver communicate with each other, you'll also need two Radio Modules, specifically, the nRF24l01+ modules.

The MCU used in this project is a Raspberry Pi Pico, due to it's immense bang for your buck.

# Parts

- 2x [nRF24l01+](https://de.aliexpress.com/item/1005006179466246.html?spm=a2g0o.order_list.order_list_main.172.84035c5fhxKu8g&gatewayAdapt=glo2deu)
- 1x [H Bridge L298N](https://de.aliexpress.com/item/1380626808.html?spm=a2g0o.order_list.order_list_main.269.381d5c5fzxfwu8&gatewayAdapt=glo2deu)
- 2x [DC Motors](https://de.aliexpress.com/item/1005005620169113.html?spm=a2g0o.order_list.order_list_main.293.381d5c5fzxfwu8&gatewayAdapt=glo2deu)
- 1x [IR Sensor](https://de.aliexpress.com/item/1005006385279953.html?spm=a2g0o.order_list.order_list_main.317.381d5c5fzxfwu8&gatewayAdapt=glo2deu)
- Insulated Wires

  - You don't want to create a short circuit between the wires of the motors, so they need to be insulted. Strip the ends of the wires to connect them to the H-Bridge.

  ## 3D printed parts

  I printed everything using the Bambu Lab P1S with the AMS module attached. For the filament, I used normal PLA material and glow in the dark PLA for the wheels.
