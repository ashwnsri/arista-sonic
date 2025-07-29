# Copyright (c) 2025 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

from ...core.psu import PsuModel, PsuIdent

from . import PmbusPsu
from .helper import psuDescHelper, Position

class FlexBmr313(PsuModel):
   CAPACITY = 1000
   AUTODETECT_PMBUS = False

   MANUFACTURER = ''.join(chr(c) for c in [0x1a, 0x0])
   PMBUS_ADDR = 0x10
   PMBUS_CLS = PmbusPsu
   IDENTIFIERS = [
      PsuIdent(''.join(chr(c) for c in [0x60, 0x0]), 'BMR313-48V-12V', None),
   ]
   DESCRIPTION = psuDescHelper(
      sensors=[
          ('internal', Position.OTHER, 100, 120, 130),
      ],
      hasFans=False,
      outputMinVoltage=11.25,
      outputMaxVoltage=13.39
   )

class FlexBmr313Addr18(FlexBmr313):
   PMBUS_ADDR = 0x12

class DeltaU50su(FlexBmr313):
   MANUFACTURER = 'DELTA' + chr(0x0)
   IDENTIFIERS = [
      PsuIdent('U50SU4P180PMDAF', 'U50SU-48V-12V', None),
   ]

class DeltaU50suAddr18(DeltaU50su):
   PMBUS_ADDR = 0x12
