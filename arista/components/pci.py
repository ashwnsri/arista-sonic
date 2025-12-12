
from ..core.quirk import Quirk
from ..core.utils import inSimulation

from ..drivers.pci import PciConfig

class EcrcPciQuirk(Quirk):
   description = "Enable ECRC"
   when = Quirk.When.AFTER
   def run(self, component):
      if inSimulation():
         return
      config = PciConfig(component.addr)
      aer = config.aerCapability()
      aer.ecrcGene(True)
      aer.ecrcChke(True)
