from lib.redux import create_store, combine_reducers, apply_middleware
from .reducers.sensors import Sensors
from .reducers.runtime import Runtime, SET_BOOT_TIMESTAMP
from .reducers.controls import Controls, PORT_PUMP_BUCKET, PORT_PUMP_RESERVOIR, PORT_LIGHTS, PORT_AUX, MASK, PINS
from .reducers.eventloop import EventLoop
import actions.sensors
from unittest.mock import MagicMock, Mock
import sensorloop
import lib.datadog

def test_action_updateComplete_shouldHaveCorrectType():

  pin = MagicMock()
  pin.value = MagicMock()
  Pin = Mock(return_value=pin)

  store = create_store(combine_reducers({
    'sensors': Sensors(),
    'runtime': Runtime(env=MagicMock()),
    'controls': Controls(),
    'eventloop': EventLoop(),
  }))
  
  ds18x20 = MagicMock()
  onewire = MagicMock()
  dht = MagicMock()
  ADC = MagicMock()
  Pin = MagicMock()
  gc = MagicMock()
  time = MagicMock()
  # datadog = MagicMock()
  requests = MagicMock()
  logger = MagicMock()
  watchdog = MagicMock()
  machine = MagicMock()

  time.time.return_value = 0
  time.localtime.return_value = (2020, 12, 24, 3, 24, 13, 3, 359, 0)

  gc.mem_free.return_value = 3
  gc.mem_alloc.return_value = 3
  # DS18X20.

  DHT22 = MagicMock()
  dht.DHT22.return_value = DHT22
  DHT22.temperature.return_value = 96
  DHT22.humidity.return_value = 96
  
  a = MagicMock()
  a.read.return_value = 1
  ADC.return_value = a

  store['dispatch']({
    'type': SET_BOOT_TIMESTAMP,
    'value': time.time()
  })
  
  tick = sensorloop.setup(
    dispatch=store['dispatch'], 
    getState=store['get_state'],
    ds18x20=ds18x20, 
    onewire=onewire,
    dht=dht,
    ADC=ADC,
    Pin=Pin,
    gc=gc,
    time=time,
    datadog=lib.datadog,
    requests=requests,
    logger=logger,
    watchdog=watchdog,
    machine=machine,
  )

  tick(None)

  # print(ds18x20.mock_calls)

  # state = store['get_state']()
  # import json
  # print('abc', json.dumps(state, sort_keys=True, indent=4))
  # assert False  
