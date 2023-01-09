"""
Module      main.py
Author      2023-01-01 Charles Geiser (https://www.dodeka.ch)

Purpose     Shows how to debounce a pushbutton and use its
            callbacks onClick(), onLongClick() and onDoubleClick() 

Board       ESP8266
Firmware    micropython from https://micropython.org

Wiring      
                                USB 
                    .-----------I...I-----------.              GPIO14  
                    | ( )   [o] |   | [o]   ( ) |                ^
                    |     Flash '---' Reset     |                |     
                    o 3V3                   Vin o        _T_     |    ___                      
                    o GND                   GND o--------o o-----+---|___|----> Vcc                                    
            ~GPIO1  o TX                    RST o                     220    
            ~GPIO3  o RX                     EN o                  
            ~GPIO15 o D8                    3V3 o                      
            ~GPIO13 o D7                    GND o                        
            ~GPIO12 o D6                    CLK o GPIO6  SCLK              Pushbutton          
            ~GPIO14 o D5                    SD0 o GPIO7  MISO               .------.   
                    o GND    ...........    CMD o GPIO11 CS       GPIO14 <--o      |
                    o 3V3   I           I   SD1 o GPIO8  MOSI        Vcc <--o  [o] | 
BUILTIN LED ~GPIO2  o D4    I  ESP8266  I   SD2 o GPIO9~             GND <--o      |
            ~GPIO0  o D3    I           I   SD3 o GPIO10~                   '------' 
            ~GPIO4  o D2    I           I   RSV o
            ~GPIO5  o D1    I           I   RSV o
             GPIO16 o D0    I...........I   AD0 o ADC0
                    |       |  _   _  | |       |
                    | ( )   |_| |_| |_|_|   ( ) |
                    '---------------------------'
"""
from machine import Pin
from debouncedButton import DebouncedButton
import time

btnPin = Pin(14, Pin.IN) # get a pin object for the pushbutton

LEDBUILTIN = const(2)
led = Pin(LEDBUILTIN, Pin.OUT)

# define the button callbacks for the events click, longclick and doubleclick
def onClick():
    print('onClick called')

def onLongClick():
    print('onLongClick called')

def onDoubleClick():
    print('onDoubleClick called')

""" 
    Returns true when the specified time has elapsed
    msCycle = [msPrevious, msCycle] is a globally defined list
    which holds the previus ticks_ms and the ms to wait
"""
def waitIsOver(msCycle):
    if (time.ticks_ms() - msCycle[0] >= msCycle[1]):
        msCycle[0] = time.ticks_ms()
        return True
    else:
        return False

btn = DebouncedButton(btnPin)       # get a debounced button object
btn.cbOnClick = onClick             # and install the callbacks
btn.cbOnLongClick = onLongClick
btn.cbOnDoubleClick = onDoubleClick

# period and pulsewidth for the blinking led
period = 1000
pulsewidth = 50

while True:
    btn.loop()  # query the button for click events
    led.value(0 if (time.ticks_ms()) % period < pulsewidth else 1) # blink the led
