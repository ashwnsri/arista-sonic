import pytest

from ...core.pci import (
   DownstreamPciPort,
   PciBridge,
   PciPort,
   PciRoot,
   PciSwitch,
   PciSysfsPath,
   RootPciBridge,
   RootPciPort,
   UpstreamPciPort,
)
from ...tests.testing import patch

from .helpers import classname, getAllSystems

@pytest.mark.parametrize('platform', getAllSystems(), ids=classname)
def testSetup(platform):
   mocks = []
   for c in platform.iterComponents():
      mocks.append(patch.object(c, 'setup').start())

   platform.setup()

   for m in mocks:
      m.assert_called_once()

@pytest.mark.parametrize('platform', getAllSystems(), ids=classname)
def testPciAddrDuplication(platform):
   pciElements = (
      DownstreamPciPort,
      PciBridge,
      PciPort,
      PciRoot,
      PciSwitch,
      RootPciBridge,
      RootPciPort,
      UpstreamPciPort
   )
   sysfsSet = set()
   for c in platform.iterComponents(filters=None):
      if not isinstance(c, pciElements) and isinstance(c.addr, PciSysfsPath):
         sysfsPath = c.addr.getSysfsPath()
         assert sysfsPath not in sysfsSet
         sysfsSet.add(sysfsPath)
