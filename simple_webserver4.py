import os
from time import sleep
import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from smbus import SMBus
import board

# import digitalio # For use with SPI
import busio
import adafruit_bmp280

host_name = '192.168.0.14'  # Change this to your Raspberry Pi IP address
host_port = 8000
addr = 0x8 # bus address
bus = SMBus(1) # indicates /dev/ic2-1
# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
# change this to match the location's pressure (hPa) at sea level
bmp280.sea_level_pressure = 1013.25

class MyServer(BaseHTTPRequestHandler):
    """ A special implementation of BaseHTTPRequestHander for reading data from
        and control GPIO of a Raspberry Pi
    """

    def do_HEAD(self):
        """ do_HEAD() can be tested use curl command
            'curl -I http://server-ip-address:port'
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """ do_GET() can be tested using curl command
            'curl http://server-ip-address:port'
        """
        html = '''
           <html>
           <body style="width:960px; margin: 20px auto;">
           <h1>Welcome to my Raspberry Pi</h1>
           <p>Current CPU temperature is {}</p>
           <p>BMP280 Tempurature is {:.1f}</p>
           <p>BMP280 Pressure is {:.1f}</p>
           <p>Turn LED: <a href="/on">On</a> <a href="/off">Off</a></p>
           <div id="led-status"></div>
           <script>
               document.getElementById("led-status").innerHTML="{}";
           </script>
           </body>
           </html>
        '''
        temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
        self.do_HEAD()
        status = ''
        if self.path=='/on':
            bus.write_byte(addr, 0x1) # switch it on
            status='LED is On'
        elif self.path=='/off':
            bus.write_byte(addr, 0x0) # switch it off
            status='LED is Off'
        x = bmp280.temperature
        x = (x*9.0/5.0) + 32.0
        self.wfile.write(html.format(temp[5:], x, bmp280.pressure, status).encode("utf-8"))
        print("Time = ", datetime.datetime.now())
        print("Temperature: %0.1f F" % x)
        print("Pressure: %0.1f hPa" % bmp280.pressure)
        print("Altitude = %0.2f meters" % bmp280.altitude)
        print(status)

if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
