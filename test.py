import time
import logging
from display import Display
import pictures as pics
import hifiberry as hifi

# Display functions
def get_formatted_title(title):
    if len(title) > 16:
        formatted_title = title[:13]  + "..."
    else:
        formatted_title = title
    return formatted_title

def get_time():
    current_time = time.strftime("%H:%M")
    return current_time

# Main function
def main():

    logging.basicConfig(filename='controller.log', level=logging.DEBUG)
    disp = Display(LCD_CS=8,LCD_RST=25,LCD_A0=24,LCD_CLK=11,LCD_SI=10)
    hifi_url = "http://127.0.0.1:81"

    disp.lcd_clear()
    while True:
        current = hifi.get_status(hifi_url)
        logging.debug("type:" + current["type"] + " - title: " + current["title"])
        disp.lcd_clear()
        logging.debug("updating display")
        disp.lcd_ascii168_string(0, 4, get_formatted_title(current["title"]))
        disp.lcd_ascii168_string(0, 6, current["artist"])
        disp.lcd_picture(2,0,pics.SPOT28,28)
        # disp.lcd_picture(0,0,pics.SPOTIFY,32)
        disp.lcd_ascii168_string(50, 1, get_time())
        if current["state"] == "paused":
            disp.lcd_picture(112,1,pics.PAUSE,8)
        elif  current["state"] == "playing":
            disp.lcd_picture(112,1,pics.PLAY,8)
        time.sleep(2)

main()