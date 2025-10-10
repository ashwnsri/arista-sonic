
import subprocess

from .log import getLogger
from .utils import inSimulation

logging = getLogger(__name__)

class Quirk(object):

   DESCRIPTION = ''
   DELAYED = False

   def __str__(self):
      return self.DESCRIPTION or super().__str__()

   def run(self, component):
      raise NotImplementedError

class QuirkDesc(Quirk): # pylint: disable=abstract-method
   def __init__(self, description):
      self.description = description

   def __str__(self):
      if self.description:
         return self.description
      return super().__str__()

class QuirkCmd(QuirkDesc):
   def __init__(self, cmd, description):
      super().__init__(description)
      self.cmd = cmd

   def run(self, component):
      if not inSimulation():
         subprocess.check_output(self.cmd)

class PciConfigQuirk(QuirkCmd): # TODO: reparent when using PciTopology
   def __init__(self, addr, expr, description):
      super().__init__(['setpci', '-s', str(addr), expr], description)
      self.addr = addr
      self.expr = expr

class RegMapSetQuirk(Quirk):
   DELAYED = True
   REG_NAME = None
   REG_VALUE = None
   def __init__(self):
      assert self.DESCRIPTION
      assert self.REG_NAME
      assert self.REG_VALUE

   def run(self, component):
      if inSimulation():
         return
      getattr(component.driver.regs, self.REG_NAME)(self.REG_VALUE)
