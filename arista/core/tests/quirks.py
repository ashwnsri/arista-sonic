import pytest

from ..quirk import (
   Quirk,
   QuirkCmd,
   RegMapSetQuirk,
)

from .helpers import classname, getAllFixedSystems

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
