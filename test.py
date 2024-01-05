import time
import logging
from display import Display
import pictures as pics
import hifiberry as hifi

# Display functions
def get_formatted_title(title):
    if len(title) > 16:
        formatted_title = title[:15]  + "-"
    else:
        formatted_title = title
    return formatted_title

# Main function
def main():

    logging.basicConfig(filename='controller.log', level=logging.DEBUG)
    disp = Display(LCD_CS=8,LCD_RST=25,LCD_A0=24,LCD_CLK=11,LCD_SI=10)
    hifi_url = "http://127.0.0.1:81"

    disp.lcd_clear()
    current = ""
    while True:
        new_current = hifi.get_status(hifi_url)
        if current != new_current:
            current = hifi.get_status(hifi_url)
            disp.lcd_clear()
            disp.lcd_ascii168_string(0, 4, get_formatted_title(current["title"]))
            disp.lcd_ascii168_string(0, 6, current["artist"])
            if current["type"] == "spotify":
                disp.lcd_picture(2,0,pics.SPOT28,28)
            else:
                disp.lcd_picture(6,1,pics.BT,20)
            disp.lcd_ascii168_string(46, 1, current["time"])
            if current["state"] == "paused":
                disp.lcd_picture(112,1,pics.PAUSE,8)
            elif  current["state"] == "playing":
                disp.lcd_picture(112,1,pics.PLAY,8)
        time.sleep(2)

main()