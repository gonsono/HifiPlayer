import time
import logging
from display import Display
import pictures as pics
from hifiberry import HifiBerry

# Display functions
def get_formatted_title(title):
    if len(title) > 16:
        formatted_title = title[:15]  + "-"
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
    hifi = HifiBerry()
    disp.lcd_clear()
    current_time = get_time()

    while True:
        refresh = False
        # Detect change in hifi object
        hifi_hash = hash(frozenset(vars(hifi).items))
        hifi.update_status()
        new_hifi_hash = hash(frozenset(vars(hifi).items))
        refresh = True if hifi_hash != new_hifi_hash

        # Detect change in time
        if current_time != get_time():
            current_time = get_time()
            refresh = True

        if refresh:
            disp.lcd_clear()
            disp.lcd_ascii168_string(0, 4, get_formatted_title(hifi.title))
            disp.lcd_ascii168_string(0, 6, hifi.artist)

            if hifi.type == "spotify":
                disp.lcd_picture(2,0,pics.SPOT28,28)
            elif hifi.type == "none":
                disp.lcd_picture(6,1,pics.NOTE,20)
            else:
                disp.lcd_picture(6,1,pics.BT,20)

            disp.lcd_ascii168_string(46, 1, get_time())

            if hifi.state == "paused":
                disp.lcd_picture(112,1,pics.PAUSE,8)
            elif  hifi.state == "playing":
                disp.lcd_picture(112,1,pics.PLAY,8)
            else:
                disp.lcd_picture(106,1,pics.HEART,20)
        time.sleep(2)

main()