
import enum
import os
import subprocess

from .log import getLogger
from .utils import inSimulation

logging = getLogger(__name__)

class Quirk:

   class When(enum.Enum):
      # apply the quirk before loading the driver
      BEFORE = 1
      # apply the quirk after the driver is loaded
      AFTER = 2
      # apply the quirk after the taking the device out of reset
      RESET = 3
      # apply the quirk once the platform in the daemon
      DELAYED = 4

   description: str = ''
   when: When = When.BEFORE

   def __str__(self):
      return self.description or f'{self.__class__.__name__}'

   def run(self, component):
      raise NotImplementedError

class QuirkDesc(Quirk): # pylint: disable=abstract-method
   def __init__(self, description=Quirk.description, when=Quirk.when):
      self.description = description
      self.when = when

class QuirkCmd(QuirkDesc):
   def __init__(self, cmd, **kwargs):
      super().__init__(**kwargs)
      self.cmd = cmd

   def run(self, component):
      if not inSimulation():
         subprocess.check_output(self.cmd)

class PciConfigQuirk(QuirkCmd): # TODO: reparent when using PciTopology
   when = Quirk.When.RESET
   def __init__(self, addr, expr, description, **kwargs):
      super().__init__(['setpci', '-s', str(addr), expr],
                       description=description, **kwargs)
      self.addr = addr
      self.expr = expr

class SysfsQuirk(QuirkDesc):
   when = Quirk.When.AFTER
   def __init__(self, entry, value, description=None, **kwargs):
      description = description or f'{entry} <- {value}'
      super().__init__(description=description, **kwargs)
      self.entry = entry
      self.value = value

   def run(self, component):
      if inSimulation():
         return

      path = os.path.join(component.addr.getSysfsPath(), self.entry)
      with open(path, "w", encoding='utf8') as f:
         f.write(f'{self.value}')

class RegMapSetQuirk(QuirkDesc):
   when = Quirk.When.DELAYED
   REG_NAME: str = None
   REG_VALUE = None

   def __init__(self, description=None, **kwargs):
      description = description or self.description or \
              f'{self.REG_NAME} <- {self.REG_VALUE}'
      super().__init__(description=description, **kwargs)

   def run(self, component):
      if inSimulation():
         return
      getattr(component.driver.regs, self.REG_NAME)(self.REG_VALUE)
