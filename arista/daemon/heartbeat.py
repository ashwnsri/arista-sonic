
from datetime import datetime, timezone
import subprocess
import time

from ..core.config import Config
from ..core.daemon import registerDaemonFeature, PollDaemonFeature
from ..core.log import getLogger
from ..core.linecard import Linecard
from ..utils.sonic_reboot import do_reboot

logging = getLogger(__name__)

@registerDaemonFeature()
class HeartbeatFeature(PollDaemonFeature):

   NAME = 'heartbeat'
   INTERVAL = 5

   @classmethod
   def runnable(cls, daemon):
      return isinstance(daemon.platform, Linecard)

   def init(self):
      # pylint: disable=attribute-defined-outside-init
      super().init()
      self.supWasAlive = False
      self.failedPingCount = 0
      self.supervisor_ip = Config().api_rpc_sup
      self.max_failed_ping = Config().linecard_heartbeat_max_failed
      self.ping_count = Config().linecard_heartbeat_ping_count
      logging.debug('Heartbeat ping initialized')

   def shutdown(self):
      # pylint: disable=unspecified-encoding
      with open('/host/reboot-cause/reboot-cause.txt', 'w') as f:
         timestamp = datetime.now(timezone.utc).ctime()
         f.write(f'Heartbeat with the Supervisor card lost [Time: {timestamp}]\n')
      subprocess.run('sync', check=False)
      subprocess.run(['/sbin/fstrim', '-av'], check=False)
      time.sleep(3)
      do_reboot(self.daemon.platform)

   def callback(self, elapsed):
      proc = subprocess.run( f'ping -W 1 -c {self.ping_count} {self.supervisor_ip}',
                             check=False)
      if proc.returncode != 0:
         if self.supWasAlive:
            if self.failedPingCount == 0:
               logging.warning('Supervisor ping unsuccessful, shutdown will be '
                               f'triggered after {self.max_failed_ping - 1} '
                               'more failed pings')
            self.failedPingCount += 1
            if self.failedPingCount >= self.max_failed_ping:
               self.shutdown()
      else:
         if not self.supWasAlive or self.failedPingCount > 0:
            logging.debug('Supervisor ping successful')
         # pylint: disable=attribute-defined-outside-init
         self.supWasAlive = True
         self.failedPingCount = 0
