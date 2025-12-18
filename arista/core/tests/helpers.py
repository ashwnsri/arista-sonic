from ..fixed import FixedSystem
from ..linecard import Linecard
from ..platform import getPlatforms, loadPlatforms

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

getAllSystems = getAllFixedSystems

def classname(obj):
   return obj.__class__.__name__
