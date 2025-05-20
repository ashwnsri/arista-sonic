from ..core.platform import registerPlatform
from ..core.port import PortLayout
from ..core.utils import incrange

from ..components.pci import EcrcPciQuirk

from ..descs.xcvr import Osfp, Sfp

from .cpu.redstart import RedstartCpu

from .quicksilver import QuicksilverBase

class QuicksilverRedstartBase(QuicksilverBase):
   SKU = []
   CPU_CLS = RedstartCpu
   def __init__(self):
      super().__init__()
      self.asic.quirks = [EcrcPciQuirk()]

@registerPlatform()
class QuicksilverP512(QuicksilverRedstartBase):
   SID = [
      'Redstart8Mk2QuicksilverP512',
      'Redstart8Mk2NQuicksilverP512',
      'Redstart832Mk2QuicksilverP512',
      'Redstart832Mk2NQuicksilverP512',
   ]
   PORTS = PortLayout(
      (Osfp(i) for i in incrange(1, 64)),
      (Sfp(i) for i in incrange(65, 66)),
   )
   HAS_TH5_EXT_DIODE = False
