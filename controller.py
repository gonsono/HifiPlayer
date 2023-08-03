import time
import threading
import signal
from multiprocessing import Queue
from display import Display
from volumio import Volumio
from rotaryencoder import RotaryEncoder
# import RPi.GPIO as GPIO
import pictures as pics

QUEUE = Queue()
EVENT = threading.Event()
DEBUG = False

# Display functions
def get_bar(duration, seek):
    nb_char = int((seek / duration) * 46)
    return bar

def get_formatted_title(title):
    if len(title) > 16:
        formatted_title = title[:13]  + "..."
    else:
        formatted_title = title
    return formatted_title

# Rotary Encoder functions

def debug(str):
    if not DEBUG:
        return
    print(str)

def on_turn(delta):
    QUEUE.put(delta)
    EVENT.set()

def consume_queue():
    while not QUEUE.empty():
        delta = QUEUE.get()
        handle_delta(delta)

def handle_delta(delta):
    if v.is_muted:
        debug("Unmuting")
        v.toggle()
    if delta == 1:
        vol = v.up()
    else:
        vol = v.down()
    print("Set volume to: {}".format(vol))

def on_press(value):
    v.toggle()
    print("Toggled mute to: {}".format(v.is_muted))
    EVENT.set()

def on_exit(a, b):
    print("Exiting...")
    encoder.destroy()
    sys.exit(0)


# Main function
def main():

    hifi = Volumio(url="http://localhost:3000")
    disp = Display(LCD_CS=8,LCD_RST=25,LCD_A0=24,LCD_CLK=11,LCD_SI=10)

    # Initialize Rotary Encoder
    enc  = RotaryEncoder(12, 16, callback=on_turn)
    # vol = Volume(hifi)
    vol = 10
    signal.signal(signal.SIGINT, on_exit)

#    try:
    while True:
        hifi.update_status()
        EVENT.wait(1200)
        consume_queue()
        EVENT.clear()
        disp.lcd_ascii168_string(0, 4, get_formatted_title(hifi.title))
        disp.lcd_ascii168_string(0, 6, hifi.artist)
        if hifi.duration > 0:
            disp.lcd_progress(34,0,0)
            for i in range(36, 36 + int((hifi.seek / hifi.duration) * 92)):
                disp.lcd_progress(i,0,1)
            if (hifi.seek < 1) and (i > 5):
                for i in range(36, 126):
                    disp.lcd_progress(i,0,3)
            disp.lcd_progress(126,0,2)
        disp.lcd_ascii168_string(0, 2, " " * (16-len(str(hifi.volume))) + str(hifi.volume))
        disp.lcd_picture(95,2,pics.VOLUME,16)
        if hifi.type == "webradio":
            disp.lcd_picture(0,0,pics.RADIO,32)
        elif hifi.type == "spotify":
            disp.lcd_picture(0,0,pics.SPOTIFY,32)
        time.sleep(0.5)
#    except Exception as e:
#        print(e)
#        GPIO.cleanup()


main()
