
from lib.redux import create_store, combine_reducers
from .reducers.sensors import Sensors, SENSOR, TEMPERATURE, HUMIDITY, UPDATED_AT, PROPERTY, VALUE, STATE, TIME
from .reducers.sensors import INSIDE_TENT, FLOATER_TOP
# Event types
from .reducers.sensors import SENSOR_UPDATE, SENSOR_UPDATE_COMPLETE
import actions.sensors
from unittest.mock import MagicMock
import time

# print(dir(old.strobe))
testSensor = INSIDE_TENT

def test_action_updateComplete_shouldHaveCorrectType():
  action = actions.sensors.updateComplete()
  assert action['type'] == SENSOR_UPDATE_COMPLETE

def test_action_switch_updateState_shouldHaveUsualSuspects():
  pin = MagicMock()
  pin.value = MagicMock(return_value=1)

  state = False
  switchActions = actions.sensors.Switch(pin=pin, name=FLOATER_TOP, time=time)
  action = switchActions.updateState(previousState=state)
  assert action['type'] == SENSOR_UPDATE
  assert action['sensor'] == FLOATER_TOP
  assert action['property'] == STATE
  assert action['value'] is True
