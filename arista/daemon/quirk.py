
from ..core.daemon import registerDaemonFeature, OneShotFeature
from ..core.log import getLogger
from ..core.quirk import Quirk

logging = getLogger(__name__)

@registerDaemonFeature()
class QuirkOneShotFeature(OneShotFeature):

   NAME = 'quirk'

   def run(self):
      for component in self.daemon.platform.iterComponents(filters=None):
         if component.quirks:
            logging.info('%s: applying quirks on %s', self, component)
            component.applyQuirks(Quirk.When.DELAYED)
