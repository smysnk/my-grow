from lib.redux import create_store, combine_reducers, apply_middleware
from unittest.mock import MagicMock, Mock
from .reducers.sensors import Sensors
from .reducers.runtime import Runtime
from .reducers.controls import Controls, PORT_PUMP_BUCKET, PORT_PUMP_RESERVOIR, PORT_LIGHTS, PORT_AUX, MASK, PINS
from .reducers.eventloop import EventLoop
import middleware
import actions.runtime
import actions.controls

# print(dir(old.strobe))

def test_store_control_portsOn_shouldSetCorrectBits():
  pin = MagicMock()
  pin.value = MagicMock()
  Pin = Mock(return_value=pin)

  portIO = middleware.PortIO(Pin=Pin)  
  store = apply_middleware(portIO.getInit())(create_store)(combine_reducers({
    'todos': Sensors(),
    'runtime': Runtime(env=MagicMock()),
    'controls': Controls(),
    'eventloop': EventLoop(),
  }))

  state = store['get_state']()
  assert (state['controls'][PINS] & PORT_PUMP_BUCKET) == 0
  assert (state['controls'][PINS] & PORT_PUMP_RESERVOIR) >> 1 == 0
  assert (state['controls'][PINS] & PORT_LIGHTS) >> 2 == 0
  assert (state['controls'][PINS] & PORT_AUX) >> 3 == 0

  store['dispatch'](actions.controls.portsOn(PORT_PUMP_BUCKET | PORT_PUMP_RESERVOIR))
  state = store['get_state']()
  assert (state['controls'][PINS] & PORT_PUMP_BUCKET) == 1
  assert (state['controls'][PINS] & PORT_PUMP_RESERVOIR) >> 1 == 1
  assert (state['controls'][PINS] & PORT_LIGHTS) >> 2 == 0
  assert (state['controls'][PINS] & PORT_AUX) >> 3 == 0

  store['dispatch'](actions.controls.portsOn(PORT_LIGHTS | PORT_AUX))
  state = store['get_state']()
  assert (state['controls'][PINS] & PORT_PUMP_BUCKET) == 1
  assert (state['controls'][PINS] & PORT_PUMP_RESERVOIR) >> 1 == 1
  assert (state['controls'][PINS] & PORT_LIGHTS) >> 2 == 1
  assert (state['controls'][PINS] & PORT_AUX) >> 3 == 1

def test_store_control_portsOff_shouldClearCorrectBits():
  pin = MagicMock()
  pin.value = MagicMock()
  Pin = Mock(return_value=pin)

  portIO = middleware.PortIO(Pin=Pin)  
  store = apply_middleware(portIO.getInit())(create_store)(combine_reducers({
    'todos': Sensors(),
    'runtime': Runtime(env=MagicMock()),
    'controls': Controls(),
    'eventloop': EventLoop(),
  }))

  store['dispatch'](actions.controls.portsOn(PORT_PUMP_BUCKET | PORT_PUMP_RESERVOIR | PORT_LIGHTS | PORT_AUX))
  state = store['get_state']()
  assert (state['controls'][PINS] & PORT_PUMP_BUCKET) == 1
  assert (state['controls'][PINS] & PORT_PUMP_RESERVOIR) >> 1 == 1
  assert (state['controls'][PINS] & PORT_LIGHTS) >> 2 == 1
  assert (state['controls'][PINS] & PORT_AUX) >> 3 == 1

  store['dispatch'](actions.controls.portsOff(PORT_LIGHTS | PORT_AUX))
  state = store['get_state']()
  assert (state['controls'][PINS] & PORT_PUMP_BUCKET) == 1
  assert (state['controls'][PINS] & PORT_PUMP_RESERVOIR) >> 1 == 1
  assert (state['controls'][PINS] & PORT_LIGHTS) >> 2 == 0
  assert (state['controls'][PINS] & PORT_AUX) >> 3 == 0

  store['dispatch'](actions.controls.portsOff(PORT_PUMP_BUCKET | PORT_PUMP_RESERVOIR))
  state = store['get_state']()
  assert (state['controls'][PINS] & PORT_PUMP_BUCKET) == 0
  assert (state['controls'][PINS] & PORT_PUMP_RESERVOIR) >> 1 == 0
  assert (state['controls'][PINS] & PORT_LIGHTS) >> 2 == 0
  assert (state['controls'][PINS] & PORT_AUX) >> 3 == 0

def test_store_control_portsEnable_shouldClearCorrectBits():
  pin = MagicMock()
  pin.value = MagicMock()
  Pin = Mock(return_value=pin)

  portIO = middleware.PortIO(Pin=Pin)  
  store = apply_middleware(portIO.getInit())(create_store)(combine_reducers({
    'todos': Sensors(),
    'runtime': Runtime(env=MagicMock()),
    'controls': Controls(),
    'eventloop': EventLoop(),
  }))

  # Clear all bits to start
  store['dispatch'](actions.controls.portsDisable(PORT_PUMP_BUCKET | PORT_PUMP_RESERVOIR | PORT_LIGHTS | PORT_AUX))
  state = store['get_state']()
  assert (state['controls'][MASK] & PORT_PUMP_BUCKET) == 0
  assert (state['controls'][MASK] & PORT_PUMP_RESERVOIR) >> 1 == 0
  assert (state['controls'][MASK] & PORT_LIGHTS) >> 2 == 0
  assert (state['controls'][MASK] & PORT_AUX) >> 3 == 0

  store['dispatch'](actions.controls.portsEnable(PORT_LIGHTS | PORT_AUX))
  state = store['get_state']()
  assert (state['controls'][MASK] & PORT_PUMP_BUCKET) == 0
  assert (state['controls'][MASK] & PORT_PUMP_RESERVOIR) >> 1 == 0
  assert (state['controls'][MASK] & PORT_LIGHTS) >> 2 == 1
  assert (state['controls'][MASK] & PORT_AUX) >> 3 == 1

  store['dispatch'](actions.controls.portsEnable(PORT_PUMP_BUCKET | PORT_PUMP_RESERVOIR))
  state = store['get_state']()
  assert (state['controls'][MASK] & PORT_PUMP_BUCKET) == 1
  assert (state['controls'][MASK] & PORT_PUMP_RESERVOIR) >> 1 == 1
  assert (state['controls'][MASK] & PORT_LIGHTS) >> 2 == 1
  assert (state['controls'][MASK] & PORT_AUX) >> 3 == 1

def test_store_control_portsDisable_shouldClearCorrectBits():
  pin = MagicMock()
  pin.value = MagicMock()
  Pin = Mock(return_value=pin)

  portIO = middleware.PortIO(Pin=Pin)  
  store = apply_middleware(portIO.getInit())(create_store)(combine_reducers({
    'todos': Sensors(),
    'runtime': Runtime(env=MagicMock()),
    'controls': Controls(),
    'eventloop': EventLoop(),
  }))

  state = store['get_state']()
  assert (state['controls'][MASK] & PORT_PUMP_BUCKET) == 1
  assert (state['controls'][MASK] & PORT_PUMP_RESERVOIR) >> 1 == 1
  assert (state['controls'][MASK] & PORT_LIGHTS) >> 2 == 1
  assert (state['controls'][MASK] & PORT_AUX) >> 3 == 1

  store['dispatch'](actions.controls.portsDisable(PORT_PUMP_BUCKET | PORT_PUMP_RESERVOIR))
  state = store['get_state']()
  assert (state['controls'][MASK] & PORT_PUMP_BUCKET) == 0
  assert (state['controls'][MASK] & PORT_PUMP_RESERVOIR) >> 1 == 0
  assert (state['controls'][MASK] & PORT_LIGHTS) >> 2 == 1
  assert (state['controls'][MASK] & PORT_AUX) >> 3 == 1

  store['dispatch'](actions.controls.portsDisable(PORT_LIGHTS | PORT_AUX))
  state = store['get_state']()
  assert (state['controls'][MASK] & PORT_PUMP_BUCKET) == 0
  assert (state['controls'][MASK] & PORT_PUMP_RESERVOIR) >> 1 == 0
  assert (state['controls'][MASK] & PORT_LIGHTS) >> 2 == 0
  assert (state['controls'][MASK] & PORT_AUX) >> 3 == 0
