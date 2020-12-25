# MCU-blink
Test program to use multiple MCUs and sensors on an I2C network

I'm just getting my feet wet and wanted something more elaborate than the Blink sketch. So I found a program on the internet that used python on a Raspberry Pi to host a local intranet web page which had buttons to turn on and off an LED connected to an RPI's GPIO pin.
https://www.e-tinkers.com/2018/04/how-to-control-raspberry-pi-gpio-via-http-web-server/

So I abstracted that by combining an example from (https://dronebotworkshop.com/i2c-arduino-raspberry-pi/), I2C Arduino to Raspberry PI communication exampe, to have a Seeeduino Xiao receive the on/off commands from the RPI and then turn the LED on/off.

But I wanted to make it more interesting by adding something else to the I2C bus. I have a Adafruit BMP280 temp/pressure I2C sensor that I connected to the existing I2C bus. I added the temperature and pressure from the BMP280 to the Web page.
