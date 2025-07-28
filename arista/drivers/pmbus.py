
from ..core.driver.kernel.i2c import I2cKernelDriver
from ..core.driver.user.gpio import GpioFuncImpl
from ..core.driver.user.i2c import I2cDevDriver

class PsuPmbusDetect(I2cDevDriver):

   MFR_ID = 0x99
   MFR_MODEL = 0x9a
   MFR_REVISION = 0x9b
   MFR_LOCATION = 0x9c
   MFR_DATE = 0x9d
   MFR_SERIAL = 0x9e

   VENDOR_MFR_ID = 0xc9
   VENDOR_MFR_MODEL = 0xca
   VENDOR_MFR_REVISION = 0xcb
   ARISTA_MFR_SKU = 0xcc

   UNKNOWN_METADATA = {
      key : 'N/A'
      for key in ['id', 'model', 'revision', 'location', 'date', 'serial']
   }

   def __init__(self, addr):
      super(PsuPmbusDetect, self).__init__(name='pmbus-detect', addr=addr)
      self.addr = addr
      self.exists_ = None
      self.id_ = None
      self.model_ = None
      self.revision_ = None
      self.location_ = None
      self.date_ = None
      self.serial_ = None

      self._prepare()

   def _prepare(self):
      if not self.exists():
         return
      try:
         # init device on page 0
         self.write_byte_data(0x00, 0x00)
      except Exception: # pylint: disable=broad-except
         pass

   def exists(self):
      if self.exists_ is None:
         self.exists_ = self.smbusPing()
      return self.exists_

   def checkId(self):
      try:
         self.id()
         return True
      except IOError:
         return False

   def _tryReadBlockStr(self, reg, default='N/A'):
      try:
         return self.read_block_data_str(reg)
      except IOError:
         return default

   def id(self):
      if self.id_ is None:
         self.id_ = self.read_block_data_str(self.MFR_ID)
      return self.id_

   def model(self):
      if self.model_ is None:
         self.model_ = self.read_block_data_str(self.MFR_MODEL)
      return self.model_

   def revision(self):
      if self.revision_ is None:
         self.revision_ = self._tryReadBlockStr(self.MFR_REVISION)
      return self.revision_

   def location(self):
      if self.location_ is None:
         self.location_ = self._tryReadBlockStr(self.MFR_LOCATION)
      return self.location_

   def date(self):
      if self.date_ is None:
         self.date_ = self._tryReadBlockStr(self.MFR_DATE)
      return self.date_

   def serial(self):
      if self.serial_ is None:
         self.serial_ = self._tryReadBlockStr(self.MFR_SERIAL)
      return self.serial_

   def getMfrMetadata(self):
      return {
         'id': self.id(),
         'model': self.model(),
         'revision': self.revision(),
         'location': self.location(),
         'date': self.date(),
         'serial': self.serial(),
      }

   def getAristaMetadata(self):
      return {
         'mfr_id': self._tryReadBlockStr(self.VENDOR_MFR_ID),
         'mfr_model': self._tryReadBlockStr(self.VENDOR_MFR_MODEL),
         'mfr_revision': self._tryReadBlockStr(self.VENDOR_MFR_REVISION),
         'sku': self._tryReadBlockStr(self.ARISTA_MFR_SKU, None),
      }

   def getMetadata(self):
      data = self.getMfrMetadata()
      if data['id'] == 'Arista':
         data['arista'] = self.getAristaMetadata()
      return data

class PmbusKernelDriver(I2cKernelDriver):
   MODULE = 'pmbus'
   NAME = 'pmbus'

   def createIsGoodFunc(self, entries):
      def func():
         # Iterate entries, return _input of the first with matching labelPrefix
         for entry, labelPrefix in entries:
            try:
               with open(self.getHwmonEntry("%s_label" % entry),
                         encoding='utf8') as f:
                  label = f.read()
                  if not label.startswith(labelPrefix):
                     continue
            except Exception: # pylint: disable=broad-except
               continue

            try:
               with open(self.getHwmonEntry("%s_input" % entry),
                         encoding='utf8') as f:
                  return 1 if int(f.read()) else 0
            except Exception: # pylint: disable=broad-except
               return 0
         return 0
      return func

   def getInputOkGpio(self):
      _isGood = self.createIsGoodFunc([('power1', 'pin'), ('in1', 'vin')])
      return GpioFuncImpl(self, _isGood, name='input_ok')

   def getOutputOkGpio(self, name=''):
      _isGood = self.createIsGoodFunc([('power2', 'pout'), ('power1', 'pout')])
      return GpioFuncImpl(self, _isGood, name='output_ok')
