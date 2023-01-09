"""
Module      debouncedButton.py
Author      2022-12-30 Charles Geiser (https://www.dodeka.ch)

Purpose     Debounces a pushbutton and handles the 3 user supplied callbacks
            onClick(), onLongClick() and onDoubleClick()
            It is assumed that - the switch bounces for no more than 50ms
                               - for a double click event at most 250 ms elapse 
                                 between the first and the second click
                               - a long click lasts longer than 300 ms
Board       ESP8266
Firmware    micropython from https://micropython.org

Usage       # Code in main program:
            from debouncedButton import DebouncedButton
            btn = DebouncedButton(Pin(0, Pin.IN))
            btn.cbOnClick = yourOnClickMethod
            bnt.cbOnLongClick = yourOnLongclickMethod
            btn.cbOnDoubleClick = yourOnDoubleClickMethod

Wiring      .-------------.     __T__
            |      GPIO 0 +-----o   o--.
            |             |            |
            |  ESP8266    |            |   
            |             |            |
            |         GND +------------+---/ GND
            '-------------'            
"""

from time import ticks_ms

class DebouncedButton:
    def __init__(self, pin):
        self._pin = pin
        self._prevState = 1
        self._btnState = 1
        self._msButtonDown = 0
        self._msFirstClick = 0
        self._msDebounce = 50 
        self._msDoubleClickGap = 250
        self._msLongClick = 300
        self._clickCount = 0

    def cbOnClick(self):        # These callbacks must be implemented by the user
        pass                    # in the main program

    def cbOnLongClick(self):
        pass

    def cbOnDoubleclick(self):
        pass

    def loop(self):
        self._prevState = self._btnState
        self._btnState = self._pin.value()    # query button, pressed is 0 (LOW)

        if (self._prevState == 1 and self._btnState == 0):    # button pressed
            self._msButtonDown = ticks_ms()                   # remember time
        elif (self._prevState == 0 and self._btnState == 1):  # button released
            if (ticks_ms() - self._msButtonDown < self._msDebounce):    # button bounces ...
                pass                                                    # ... ignore 
            elif (ticks_ms() - self._msButtonDown > self._msLongClick):     # time greater 300ms
                self.cbOnLongClick()                                        # its a long click
            else:
                self._clickCount += 1    # count the number of clicks 
                if self._clickCount == 1: 
                    self._msFirstClick = ticks_ms() # remember time only if its the 1st click
        else:
            if (self._clickCount == 1 and ticks_ms() - self._msFirstClick > self._msDoubleClickGap):  # time after 1st click is greater
                self._msFirstClick = 0   # reset remembered times                                     # than msDoubleClickGap, i.e. its a click
                self._clickCount = 0     # and clickcount
                self.cbOnClick()        # single click callback is called
            elif self._clickCount > 1:       # more than 1 click occured inbetween msDoubleclickGab
                self._msFirstClick = 0       # reset remembered time of first click
                self._clickCount = 0         #       and also the clickcount
                self.cbOnDoubleClick()      # double click callback is called
