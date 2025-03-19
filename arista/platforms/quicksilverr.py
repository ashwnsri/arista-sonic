from ..core.platform import registerPlatform
from ..core.port import PortLayout
from ..core.quirk import PciConfigQuirk
from ..core.utils import incrange
from ..descs.xcvr import Osfp, Sfp
from .cpu.redstart import RedstartCpu
from .quicksilver import QuicksilverBase
class QuicksilverRedstartBase(QuicksilverBase):
   SKU = []
   CPU_CLS = RedstartCpu
   def __init__(self):
      super().__init__()
      asicBridgeAddr = self.asic.addr.port.upstream.addr
      self.asic.quirks = [
         PciConfigQuirk(asicBridgeAddr, 'CAP_EXP+0x30.W=0x3',
                        'Force pcie link speed to Gen 3'),
         PciConfigQuirk(asicBridgeAddr, 'CAP_EXP+0x10.W=0x6',
                        'Trigger pcie link retraining'),
      ]
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
