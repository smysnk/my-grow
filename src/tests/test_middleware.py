from lib.redux import create_store, combine_reducers, apply_middleware
from unittest.mock import MagicMock, Mock
from .reducers.sensors import Sensors
from .reducers.runtime import Runtime
from .reducers.controls import Controls, PORT_PUMP_BUCKET, PORT_PUMP_RESERVOIR, PORT_LIGHTS, PORT_AUX
from .reducers.eventloop import EventLoop
import middleware
import actions.runtime
import actions.controls

# print(dir(old.strobe))

def test_portIO_default_shouldSetEmergencyIndicatorPinFalse():

  pin = MagicMock()
  pin.value = MagicMock()
  Pin = Mock(return_value=pin)

  portIO = middleware.PortIO(Pin=Pin)
  store = apply_middleware(portIO.getInit())(create_store)(combine_reducers({
    'todos': Sensors(),
    'runtime': Runtime(env=MagicMock()),
    'eventloop': EventLoop(),
  }))

  store['dispatch'](dict(type='ADD_TODO', text='Hello'))
  pin.value.assert_called_once_with(False)


def test_portIO_store_action_setEmergencyShutoff_shouldSetEmergencyIndicatorPinTrue():

  pin = MagicMock()
  pin.value = MagicMock()
  Pin = Mock(return_value=pin)

  portIO = middleware.PortIO(Pin=Pin)

  store = apply_middleware(portIO.getInit())(create_store)(combine_reducers({
    'todos': Sensors(),
    'runtime': Runtime(env=MagicMock()),
    'eventloop': EventLoop(),
  }))

  store['dispatch'](actions.eventloop.emergencyShutoff(True))
  pin.value.assert_called_once_with(True)

def test_portIO_store_startup_shouldInitiatePins():

  def Pin(a, b):
    pin = MagicMock()
    pin.value = MagicMock()
    return pin
 
  Pin.OUT = 'OUT'

  portIO = middleware.PortIO(Pin=Pin)
  store = apply_middleware(portIO.getInit())(create_store)(combine_reducers({
    'todos': Sensors(),
    'runtime': Runtime(env=MagicMock()),
    'controls': Controls(),
    'eventloop': EventLoop(),
  }))

  store['dispatch']({ 'type': 'STARTUP' })
  state = store['get_state']()
  for pin in portIO.pins:
    pin['io'].value.assert_called_once_with(1) # Should be 1 because relay boards logis is inverted


def test_portIO_store_shouldSetPinsCorrectly():
  def Pin(a, b):
    pin = MagicMock()
    pin.value = MagicMock()
    return pin
 
  Pin.OUT = 'OUT'

  portIO = middleware.PortIO(Pin=Pin)
  store = apply_middleware(portIO.getInit())(create_store)(combine_reducers({
    'todos': Sensors(),
    'runtime': Runtime(env=MagicMock()),
    'controls': Controls(),
    'eventloop': EventLoop(),
  }))

  store['dispatch'](actions.controls.portsOn(PORT_PUMP_BUCKET | PORT_LIGHTS))
  portIO.pins[0]['io'].value.assert_called_once_with(0) # Bucket
  portIO.pins[1]['io'].value.assert_called_once_with(1) # Reservoir
  portIO.pins[2]['io'].value.assert_called_once_with(0) # Lights
  portIO.pins[3]['io'].value.assert_called_once_with(1) # Aux

  for pin in portIO.pins: pin['io'].value.reset_mock()
  store['dispatch'](actions.controls.portsOn(PORT_AUX))
  portIO.pins[0]['io'].value.assert_called_once_with(0) # Bucket
  portIO.pins[1]['io'].value.assert_called_once_with(1) # Reservoir
  portIO.pins[2]['io'].value.assert_called_once_with(0) # Lights
  portIO.pins[3]['io'].value.assert_called_once_with(0) # Aux

  for pin in portIO.pins: pin['io'].value.reset_mock()
  store['dispatch'](actions.controls.portsOn(PORT_PUMP_RESERVOIR))
  portIO.pins[0]['io'].value.assert_called_once_with(0) # Bucket
  portIO.pins[1]['io'].value.assert_called_once_with(0) # Reservoir
  portIO.pins[2]['io'].value.assert_called_once_with(0) # Lights
  portIO.pins[3]['io'].value.assert_called_once_with(0) # Aux

def test_portIO_store_shouldSetPinsCorrectlyWithMask():
  def Pin(a, b):
    pin = MagicMock()
    pin.value = MagicMock()
    return pin
 
  Pin.OUT = 'OUT'

  portIO = middleware.PortIO(Pin=Pin)
  store = apply_middleware(portIO.getInit())(create_store)(combine_reducers({
    'todos': Sensors(),
    'runtime': Runtime(env=MagicMock()),
    'controls': Controls(),
    'eventloop': EventLoop(),
  }))

  store['dispatch'](actions.controls.portsOn(PORT_PUMP_BUCKET | PORT_PUMP_RESERVOIR | PORT_LIGHTS | PORT_AUX))
  
  for pin in portIO.pins: pin['io'].value.reset_mock()
  store['dispatch'](actions.controls.portsDisable(PORT_PUMP_BUCKET | PORT_LIGHTS))
  portIO.pins[0]['io'].value.assert_called_once_with(1) # Bucket
  portIO.pins[1]['io'].value.assert_called_once_with(0) # Reservoir
  portIO.pins[2]['io'].value.assert_called_once_with(1) # Lights
  portIO.pins[3]['io'].value.assert_called_once_with(0) # Aux

  for pin in portIO.pins: pin['io'].value.reset_mock()
  store['dispatch'](actions.controls.portsDisable(PORT_PUMP_RESERVOIR))
  portIO.pins[0]['io'].value.assert_called_once_with(1) # Bucket
  portIO.pins[1]['io'].value.assert_called_once_with(1) # Reservoir
  portIO.pins[2]['io'].value.assert_called_once_with(1) # Lights
  portIO.pins[3]['io'].value.assert_called_once_with(0) # Aux

  for pin in portIO.pins: pin['io'].value.reset_mock()
  store['dispatch'](actions.controls.portsDisable(PORT_AUX))
  portIO.pins[0]['io'].value.assert_called_once_with(1) # Bucket
  portIO.pins[1]['io'].value.assert_called_once_with(1) # Reservoir
  portIO.pins[2]['io'].value.assert_called_once_with(1) # Lights
  portIO.pins[3]['io'].value.assert_called_once_with(1) # Aux
  
  # pin['io'].value.assert_called_once_with(1) # Should be 1 because relay boards logis is inverted
  # print(portIO.pins)

  # import json
  # print('abc', json.dumps(state, sort_keys=True, indent=4))
  # assert False == True

