from display import Display
from volumio import Volumio

def get_bar(duration, seek):
    nb_dash = int((seek / duration) * 14)
    bar = "-" * nb_dash + " " * (14 - nb_dash)
    return bar

def main():

    hifi = Volumio()
    disp = Display(LCD_CS=8,LCD_RST=25,LCD_A0=24,LCD_CLK=11,LCD_SI=10)
    try:
        while True:
            disp.lcd_ascii168_string(0, 4, hifi.title)
            disp.lcd_ascii168_string(0, 6, hifi.artist)
            disp.lcd_ascii168_string(0, 0, "[" + get_bar(hifi.duration, hifi.seek) + "]")
            disp.lcd_ascii168_string(0, 2, "Spotify  ||   " + str(hifi.volume))
            time.sleep(1.0)
    except:
        GPIO.cleanup()


main()