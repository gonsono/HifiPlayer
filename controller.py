import time
from display import Display
from volumio import Volumio
import RPi.GPIO as GPIO

def get_bar(duration, seek):
    nb_char = int((seek / duration) * 46)
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
#    try:
    while True:
        hifi.update_status()
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
        disp.lcd_picture(95,2,disp.bmp_volume,16)
        if hifi.type == "webradio":
            disp.lcd_picture(0,0,disp.bmp_radio,32)
        elif hifi.type == "spotify":
            disp.lcd_picture(0,0,disp.bmp_spotify,32)
        time.sleep(0.5)
#    except Exception as e:
#        print(e)
#        GPIO.cleanup()


main()
