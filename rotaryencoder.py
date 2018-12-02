#!/usr/bin/env python3

import os
import signal
import subprocess
import sys
import threading

from RPi import GPIO
from multiprocessing import Queue

class RotaryEncoder:

  def __init__(self, gpioA, gpioB, callback=None, buttonPin=None, buttonCallback=None):

    self.lastGpio = None
    self.gpioA    = gpioA
    self.gpioB    = gpioB
    self.callback = callback

    self.gpioButton     = buttonPin
    self.buttonCallback = buttonCallback

    self.levA = 0
    self.levB = 0

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.gpioA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(self.gpioB, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(self.gpioA, GPIO.BOTH, self._callback)
    GPIO.add_event_detect(self.gpioB, GPIO.BOTH, self._callback)

    if self.gpioButton:
      GPIO.setup(self.gpioButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
      GPIO.add_event_detect(self.gpioButton, GPIO.FALLING, self._buttonCallback, bouncetime=500)


  def destroy(self):
    GPIO.remove_event_detect(self.gpioA)
    GPIO.remove_event_detect(self.gpioB)
    GPIO.cleanup()

  def _buttonCallback(self, channel):
    self.buttonCallback(GPIO.input(channel))

  def _callback(self, channel):
    level = GPIO.input(channel)
    if channel == self.gpioA:
      self.levA = level
    else:
      self.levB = level

    # Debounce.
    if channel == self.lastGpio:
      return

    # When both inputs are at 1, we'll fire a callback. If A was the most
    # recent pin set high, it'll be forward, and if B was the most recent pin
    # set high, it'll be reverse.
    self.lastGpio = channel
    if channel == self.gpioA and level == 1:
      if self.levB == 1:
        self.callback(1)
    elif channel == self.gpioB and level == 1:
      if self.levA == 1:
        self.callback(-1)

class Volume:
  """
  A wrapper API for interacting with the volume settings on the RPi.
  """
  MIN = 0
  MAX = 100
  INCREMENT = 2

  def __init__(self, volumio):
    # Set an initial value for last_volume in case we're muted when we start.
    self.last_volume = volumio.volume
    self._sync()

  def up(self):
    """
    Increases the volume by one increment.
    """
    return self.change(self.INCREMENT)

  def down(self):
    """
    Decreases the volume by one increment.
    """
    return self.change(-self.INCREMENT)

  def change(self, delta):
    v = self.volume + delta
    v = self._constrain(v)
    return self.set_volume(v)

  def set_volume(self, v):
    """
    Sets volume to a specific value.
    """
    self.volume = self._constrain(v)
    #os.system('volumio volume ' + str(v))
    volumio.set_volume(v)
    self._sync(volumio.volume)
    return self.volume

  def toggle(self):
    """
    Toggles muting between on and off.
    """
    if self.is_muted:
      os.system('volumio volume unmute')
    else:
      # We're about to mute ourselves, so we should remember the last volume
      # value we had because we'll want to restore it later.
      self.last_volume = self.volume
      os.system('volumio volume mute')

    self._sync(volumio.volume)
    if not self.is_muted:
      # If we just unmuted ourselves, we should restore whatever volume we
      # had previously.
      self.set_volume(self.last_volume)
    return self.is_muted

  def status(self):
    if self.is_muted:
      return "{}% (muted)".format(self.volume)
    return "{}%".format(self.volume)

  def _sync(self, output=None):
    self.is_muted = volumio.mute
    self.volume = volumio.volume

  # Ensures the volume value is between our minimum and maximum.
  def _constrain(self, v):
    if v < self.MIN:
      return self.MIN
    if v > self.MAX:
      return self.MAX
    return v

