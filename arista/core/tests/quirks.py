import pytest

from ..fixed import FixedSystem
from ..linecard import Linecard
from ..platform import getPlatforms, loadPlatforms
from ..quirk import (
   Quirk,
   QuirkCmd,
   RegMapSetQuirk,
)

def getAllFixedSystems():
   loadPlatforms()
   for platformCls in getPlatforms():
      if issubclass(platformCls, Linecard) and platformCls.CPU_CLS:
         yield platformCls()
      elif issubclass(platformCls, FixedSystem):
         yield platformCls()
      # NOTE: this leaves behind the following products
      # - chassis
      # - fabric cards
      # - linecards without CPUs

def classname(obj):
   return obj.__class__.__name__

def _testQuirk(quirk, component):
   assert isinstance(quirk, Quirk)
   assert isinstance(str(quirk), str)
   assert str(quirk)
   assert isinstance(quirk.when, Quirk.When)

   if isinstance(quirk, QuirkCmd):
      assert quirk.cmd
      assert isinstance(quirk.cmd, list)

   if isinstance(quirk, RegMapSetQuirk):
      assert quirk.REG_NAME
      assert quirk.REG_VALUE
      assert hasattr(component.driver.regs, quirk.REG_NAME)

   quirk.run(component)

@pytest.mark.parametrize('platform', getAllFixedSystems(), ids=classname)
def testQuirks(platform):
   for component in platform.iterComponents(None):
      for quirk in component.quirks:
         _testQuirk(quirk, component)
