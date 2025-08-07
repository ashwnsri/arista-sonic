
from .log import getLogger

logging = getLogger(__name__)

class LazyArgsStr:
   def __init__(self, args, kwargs):
      self.args = args
      self.kwargs = kwargs

   def __str__(self):
      def format_arg(a):
         if isinstance(a, int):
            return f'{a:#04x}'
         return str(a)

      return ', '.join(s for s in (
         ', '.join(format_arg(a) for a in self.args),
         ', '.join(f'{k}={v}' for k, v in self.kwargs.items()),
      ) if s)

def logIoWrite(func):
   def wraps(self, *args, **kwargs):
      logging.io('%s.%s(%s)', self, func.__name__, LazyArgsStr(args, kwargs))
      return func(self, *args, **kwargs)
   return wraps

def logIoRead(func):
   def wraps(self, *args, **kwargs):
      try:
         data = func(self, *args, **kwargs)
         logging.io('%s.%s(%s): %s',
                    self, func.__name__, LazyArgsStr(args, kwargs), data)
         return data
      except Exception:
         logging.io('%s.%s(%s): ERROR',
                    self, func.__name__, LazyArgsStr(args, kwargs))
         raise
   return wraps
