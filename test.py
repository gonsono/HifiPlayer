import time
import logging
from display import Display
import pictures as pics

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

# Main function
def main():

    logging.basicConfig(filename='controller.log', level=logging.DEBUG)

    # hifi = Volumio(url="http://localhost:3000")
    hifi = {
        "type": "Spotify",
        "title": "Pump up the jam",
        "artist": "Technotronic"
    }
    disp = Display(LCD_CS=8,LCD_RST=25,LCD_A0=24,LCD_CLK=11,LCD_SI=10)

#    try:
    while True:
        hifi.update_status()
        logging.debug("type:" + hifi["type"] + " - title: " + hifi["title"])
        disp.lcd_clear()
        logging.debug("updating display")
        disp.lcd_ascii168_string(0, 4, get_formatted_title(hifi["title"]))
        disp.lcd_ascii168_string(0, 6, hifi["artist"])
        disp.lcd_picture(0,0,pics.SPOTIFY,32)
        time.sleep(2)

main()