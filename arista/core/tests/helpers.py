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

def isChildComponentOf(component, parent):
   while parent:
      if component in parent.components:
         return True
      parent = parent.parent
   return False

def isAncestorToComponent(component, ancestor):
   while component:
      if component == ancestor:
         return True
      component = component.parent
   return False
