
from .component import Component
from ..quirk import QuirkDesc

class I2cRegisterQuirk(QuirkDesc): # pylint: disable=abstract-method
   def __init__(self, addr, data, description=None, **kwargs):
      description = description or f'{addr} <- {data}'
      super().__init__(description=description, **kwargs)
      self.addr = addr
      self.data = data

class I2cByteQuirk(I2cRegisterQuirk):
   def run(self, component):
      component.driver.write_byte_data(self.addr, self.data)

class I2cBlockQuirk(I2cRegisterQuirk):
   def run(self, component):
      component.driver.write_bytes([self.addr, len(self.data)] + self.data)

class I2cComponent(Component):
   pass
