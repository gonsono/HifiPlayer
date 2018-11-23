import time
from display import Display
from volumio import Volumio
import RPi.GPIO as GPIO

def get_bar(duration, seek):
    nb_dash = int((seek / duration) * 14)
    bar = "-" * nb_dash + " " * (14 - nb_dash)
    return bar

def get_formatted_title(title):
    if len(title) > 16:
        formatted_title = title[:13]  + "..."
    else:
        formatted_title = title
    return formatted_title

def main():

    hifi = Volumio()
    disp = Display(LCD_CS=8,LCD_RST=25,LCD_A0=24,LCD_CLK=11,LCD_SI=10)
    try:
        while True:
            hifi.update_status()
            disp.lcd_ascii168_string(0, 4, get_formatted_title(hifi.title))
            disp.lcd_ascii168_string(0, 6, hifi.artist)
            if hifi.duration > 0:
                disp.lcd_ascii168_string(0, 0, "[" + get_bar(hifi.duration, hifi.seek) + "]")
            disp.lcd_ascii168_string(0, 2, hifi.type + " " * (16-len(hifi.type+str(hifi.volume))) + str(hifi.volume))
            time.sleep(0.2)
    except:
        GPIO.cleanup()


main()
