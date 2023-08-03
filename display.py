import RPi.GPIO as GPIO
# import time
# import numpy as np
import characters as chars

class Display:
    """Display class that allow interaction with a LCD Screen based on ST7565 controller"""

    # Default values
    default_mode = "volumio"
    LCD_CS = 8
    LCD_RST = 25
    LCD_A0 = 24
    LCD_CLK = 11
    LCD_SI = 10

    def __init__(self, mode=default_mode, LCD_CS=LCD_CS, LCD_RST=LCD_RST, LCD_A0=LCD_A0, LCD_CLK=LCD_CLK, LCD_SI=LCD_SI):
        # Set default display mode
        self.mode = mode
        print("Display mode set to " + self.mode)

        # Init GPIO
        self.LCD_CS = LCD_CS
        self.LCD_RST = LCD_RST
        self.LCD_A0 = LCD_A0
        self.LCD_CLK = LCD_CLK
        self.LCD_SI = LCD_SI
        self.io_init()

        # Init display
        self.lcd_init()

    def io_init(self):
        """Initialize GPIO communication"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.LCD_CS, GPIO.OUT)
        GPIO.setup(self.LCD_RST, GPIO.OUT)
        GPIO.setup(self.LCD_A0, GPIO.OUT)
        GPIO.setup(self.LCD_CLK, GPIO.OUT)
        GPIO.setup(self.LCD_SI, GPIO.OUT)

    def lcd_init(self):
        """Initialize LCD display"""
        GPIO.output(self.LCD_CS, True)
        GPIO.output(self.LCD_RST, False)
        GPIO.output(self.LCD_RST, True)
        self.lcd_tranfer_data(0xe2, 0)  # Internal reset

        self.lcd_tranfer_data(0xa2, 0)  # Sets the LCD drive voltage bias ratio ## TODO: i set to a2 instead of a3
        ##A2: 1/9 bias
        ##A3: 1/7 bias (ST7565V)

        self.lcd_tranfer_data(0xa0, 0)  # Sets the display RAM address SEG output correspondence
        ##A0: normal
        ##A1: reverse

        self.lcd_tranfer_data(0xc8, 0)  # Select COM output scan direction
        ##C0~C7: normal direction
        ##C8~CF: reverse direction

        self.lcd_tranfer_data(0xa4, 0)  # Display all points ON/OFF
        ##A4: normal display
        ##A5: all points ON

        self.lcd_tranfer_data(0xa6, 0)  # Sets the LCD display normal/inverted
        ##A6: normal
        ##A7: inverted

        self.lcd_tranfer_data(0x2F, 0)  # select internal power supply operating mode
        ##28~2F: Operating mode

        self.lcd_tranfer_data(0x60, 0)  # Display start line set
        ##40~7F Display start address

        self.lcd_tranfer_data(0x24, 0)  # V5 voltage regulator internal resistor ratio set(contrast)
        ##20~27 small~large

        self.lcd_tranfer_data(0x81, 0)  # Electronic volume mode set
        ##81: Set the V5 output voltage

        self.lcd_tranfer_data(0x30, 0)  # Electronic volume register set
        ##00~3F: electronic volume register

        self.lcd_tranfer_data(0b10101111, 0)  # Display ON/OFF
        ##    0b10101111: ON
        ##    0b10101110: OFF
        self.lcd_clear()

    def lcd_picture(self, xPos, yPos, bmp, width):
        nb_page = len(bmp)/width
        for i in range(0, nb_page):
            self.lcd_set_page(yPos+i,xPos)
            for j in range(width*i, width*(i+1)):
                self.lcd_tranfer_data(bmp[j],1)

    def lcd_progress(self, x_pos, y_pos, char):
        """Print a progress bar on the display"""
        self.lcd_set_page(y_pos, x_pos)

        for i in range(0, 2):
            self.lcd_tranfer_data(chars.PROGRESS[char][i], 1)

        self.lcd_set_page(y_pos + 1, x_pos)
        for i in range(2, 4):
            self.lcd_tranfer_data(chars.PROGRESS[char][i], 1)

    def lcd_ascii168_string(self, x_pos, y_pos, string):
        """Print a string on the display"""
        string_len = len(string)
        for i in range(0, string_len):
            self.lcd_ascii168(x_pos + i * 8, y_pos, ord(string[i]) - 32)

    def lcd_ascii168(self, x_pos, y_pos, char):
        """Print a character on the display"""
        self.lcd_set_page(y_pos, x_pos)

        for i in range(0, 8):
            self.lcd_tranfer_data(chars.ASCII168[char][i], 1)

        self.lcd_set_page(y_pos + 1, x_pos)
        for i in range(8, 16):
            self.lcd_tranfer_data(chars.ASCII168[char][i], 1)

    def lcd_clear(self):
        """Erase the display"""
        GPIO.output(self.LCD_CS, False)
        for i in range(0, 8):
            self.lcd_set_page(i, 0)
            for j in range(0, 128):
                self.lcd_tranfer_data(0x00, 1)
        GPIO.output(self.LCD_CS, True)

    def lcd_set_page(self, page, column):
        lsb = column & 0x0f
        msb = column & 0xf0
        msb >>= 4
        msb |= 0x10
        page |= 0xb0
        self.lcd_tranfer_data(page, 0)
        self.lcd_tranfer_data(msb, 0)
        self.lcd_tranfer_data(lsb, 0)

    def lcd_tranfer_data(self, value, A0):
        GPIO.output(self.LCD_CS, False)
        GPIO.output(self.LCD_CLK, True)
        if (A0):
            GPIO.output(self.LCD_A0, True)
        else:
            GPIO.output(self.LCD_A0, False)
        self.lcd_byte(value)
        GPIO.output(self.LCD_CS, True)

    def lcd_byte(self, bits):
        tmp = bits
        for i in range(0, 8):
            GPIO.output(self.LCD_CLK, False)
            if (tmp & 0x80):
                GPIO.output(self.LCD_SI, True)
            else:
                GPIO.output(self.LCD_SI, False)
            tmp = (tmp << 1)
            GPIO.output(self.LCD_CLK, True)
