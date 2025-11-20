
from ..core.desc import HwDesc

class LedColor(object):
   GREEN = 'green'
   RED = 'red'
   AMBER = 'amber'
   BLUE = 'blue'
   PURPLE = 'purple'
   WHITE = 'white'
   CYAN = 'cyan'
   OFF = 'off'
   OTHER = 'other'

class LedInterfaceType:
   LEGACY = 0
   MONO = 1
   MULTICOLOR = 2

   @staticmethod
   def forKind(kind: int) -> int:
      if kind == LedKind.LEGACY:
         return LedInterfaceType.LEGACY
      if kind == LedKind.BLUE:
         return LedInterfaceType.MONO
      return LedInterfaceType.MULTICOLOR

class LedKind:
   LEGACY = 0
   BLUE = 1
   RA = 2
   RG = 3
   RG_F = 4
   GA = 5
   GA_F = 6
   GA_1F = 7
   RGB_P3F = 8
   RGB_8_F = 9

   _PROPERTIES = {
      LEGACY: {},
      BLUE: { 'colors': [LedColor.BLUE] },
      RA: { 'colors': [LedColor.RED, LedColor.AMBER] },
      RG: { 'colors': [LedColor.RED, LedColor.GREEN] },
      RG_F: { 'colors': [LedColor.RED, LedColor.GREEN], 'blink': True },
      GA: { 'colors': [LedColor.GREEN, LedColor.AMBER] },
      GA_F: { 'colors': [LedColor.GREEN, LedColor.AMBER], 'blink': True },
      GA_1F: { 'colors': [LedColor.GREEN, LedColor.AMBER], 'blink': True },
      RGB_P3F: { 'colors': [LedColor.RED, LedColor.GREEN, LedColor.BLUE],
                   'blink': True },
      RGB_8_F: { 'colors': [LedColor.RED, LedColor.GREEN, LedColor.BLUE],
                 'blink': True },
   }

   @staticmethod
   def desc(kind):
      return {'kind': kind} | LedKind._PROPERTIES[kind]

class LedDesc(HwDesc):
   def __init__(self, name=None, colors=None, blinking=False, **kwargs):
      super(LedDesc, self).__init__(**kwargs)
      self.name = name
      self.colors = colors
      self.blinking = blinking
