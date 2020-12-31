from unittest.mock import MagicMock, call, ANY

import lib.logger


def test_canAppendLoggers():
  time = MagicMock()
  time.dateTimeIso.return_value = '1'
  logger = lib.logger.config(time=time, include=['.*'], exclude=[], enabled=True)

  assert logger(append='1')(append='2')(append='3')('abc') == '[1][1:2:3] abc'

def test_canSpecifyCustomName():
  time = MagicMock()
  time.dateTimeIso.return_value = '1'
  logger = lib.logger.config(time=time, include=['.*'], exclude=[], enabled=True)

  assert logger(append='1')(append='2')(append='3')('abc', name='custom') == '[1][1:2:3:custom] abc'

