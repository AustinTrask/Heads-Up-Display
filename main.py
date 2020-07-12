import time
import board
import busio
import digitalio
import math
import displayio
import terminalio

from adafruit_display_text import label
import adafruit_gps
import adafruit_lsm303dlh_mag
import adafruit_displayio_ssd1306

displayio.release_displays()

button0 = digitalio.DigitalInOut(board.A0)
button0.direction = digitalio.Direction.INPUT
button0.pull = digitalio.Pull.DOWN

button1 = digitalio.DigitalInOut(board.A1)
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.DOWN

button2 = digitalio.DigitalInOut(board.A2)
button2.direction = digitalio.Direction.INPUT
button2.pull = digitalio.Pull.DOWN

button3 = digitalio.DigitalInOut(board.A3)
button3.direction = digitalio.Direction.INPUT
button3.pull = digitalio.Pull.DOWN

RX = board.RX
TX = board.TX

uart = busio.UART(TX, RX, baudrate=9600, timeout=1)
gps = adafruit_gps.GPS(uart, debug=False)


i2c = board.I2C()
mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)

display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

splash = displayio.Group(max_size=3)
display.show(splash)

color_bitmap = displayio.Bitmap(128, 32, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000000

#bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
#splash.append(bg_sprite)

last_print = time.monotonic()
current = time.monotonic()
old = current
count = 0
bearing = 0
p = math.pi

speed_unit = 1
speed_disp = 0
speed_kts = 0

def speedConvert(speed_kts, speed_unit):
    #print(speed_kts)
    if speed_unit == 0:
        speed_disp = speed_kts
        #print(speed_disp)
        unit_disp = 'KTS'
    elif speed_unit == 1:
        speed_disp = 1.151 * speed_kts
        unit_disp = 'MPH'
    elif speed_unit == 2:
        speed_disp = 1.852 * speed_kts
        unit_disp = 'KPH'
    elif speed_unit == 3:
        speed_disp = .5144 * speed_kts
        unit_disp = 'M/S'
    return(speed_disp, unit_disp)

def formatSpeed(speed_disp):
    if speed_disp < 1:
        speedForm = str(0)
    elif speed_disp < 10:
        speedForm = str(speed_disp)[:1]
    elif speed_disp < 100:
        speedForm = str(speed_disp)[:2]
    else:
        speedForm = str(speed_disp)[:3]
    return(speedForm)

def formatBearing(bearing):
    if bearing < 1:
        bearingForm = str(0)
    elif bearing < 10:
        bearingForm = str(bearing)[:1]
    elif bearing < 100:
        bearingForm = str(bearing)[:2]
    else:
        bearingForm = str(bearing)[:3]
    return(bearingForm)

def getBearing(x,y):
    #calculate bearing and return it
    if x >= 0 and y >= 0:
        bearing = (180 / p) * math.atan(y/x)
    elif x < 0:
        bearing = 180 + ((180 / p) * math.atan(y/x))
    else:
        bearing = 360 + ((180 / p) * math.atan(y/x))
    return(bearing)

while True:

    hasLock = True
    #if button0.value:
    #    speed_unit = 0
    #elif button1.value:
    #    speed_unit = 1
    #elif button2.value:
    #    speed_unit = 2
    #elif button3.value:
    #    speed_unit = 3

    current = time.monotonic()
    count = count + 1

    if uart.in_waiting > 0:
        gps_string = uart.readline()
        print(gps_string)
        if "GPRMC" in gps_string:
            old = current
            #print(gps_string)
            gps_string_conv = str(gps_string, 'ascii')
            #print(gps_string_conv)
            gps_array = gps_string_conv.split(',')
            #print(gps_array[7])
            speed_kts = float(gps_array[7])
            #print(speed_kts)

    try:
        testArray = gps_array
    except:
        hasLock = False


    if count == 2:
        count = 0

        x = mag.magnetic[0]
        y = mag.magnetic[1]

        if x == 0:
            x = 0.00001

        bearing = getBearing(x,y)

        (speed_disp, unit_disp) = speedConvert(speed_kts, speed_unit)

        speedForm = formatSpeed(speed_disp)
        bearingForm = formatBearing(bearing)

        try:
            if gps_array[4] != 'N' and gps_array[4] != 'S':
                hasLock = False
        except:
            useless = True

        if hasLock == False:
            speedForm = 'NL'

        ln1 = speedForm
        ln2 = unit_disp
        ln3 = bearingForm

        text_area1 = label.Label(terminalio.FONT, text=ln1, color=0xFFFFFF, x=41, y=10)
        text_area2 = label.Label(terminalio.FONT, text=ln2, color=0xFFFFFF, x=66, y=10)
        text_area3 = label.Label(terminalio.FONT, text=ln3, color=0xFFFFFF, x=54, y=20)

        splash = displayio.Group(max_size=3)
        display.show(splash)

        splash.append(text_area1)
        splash.append(text_area2)
        splash.append(text_area3)

    time.sleep(.05)