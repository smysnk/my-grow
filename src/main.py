import gc, lib, json, dht, socket, machine
from machine import Pin, Timer, ADC, WDT
from .lib import redux, datadog
from . import reducers, actions, sensorloop, middleware
# import actions.sensors
from .reducers.controls import PORT_PUMP_BUCKET, PORT_PUMP_RESERVOIR, PORT_LIGHTS, PORT_AUX
from .reducers.runtime import SET_BOOT_TIMESTAMP
from .lib import ws, datadog
import onewire, ds18x20


def start(env=None, requests=None, logger=None, time=None):
  log = logger('main')
  log("Starting..")

  # Redux stuff
  r = redux.combine_reducers({
    'eventloop': reducers.eventloop.EventLoop(),
    'controls': reducers.controls.Controls(),
    'sensors': reducers.sensors.Sensors(),
    'runtime': reducers.runtime.Runtime(env),
  })

  # Setup websocket server
  channel = ws.Channel()
  server = ws.Server(channel)

  portIO = middleware.PortIO(Pin=Pin, logger=logger)
  store = redux.apply_middleware(portIO.getInit(), middleware.Broadcast(channel))(redux.create_store)(r)

  dispatch = store['dispatch']
  getState = store['get_state']

  # Will initialize the control IO pins via middleware
  dispatch({
    'type': 'STARTUP',
  })

  dispatch({
    'type': SET_BOOT_TIMESTAMP,
    'value': time.time()
  })

  # Watchdog timer - Reset ESP32 if it stops responding
  watchdog = WDT(timeout=60000) if env.settings['watchdog'] else None

  tick = sensorloop.setup(
    dispatch=dispatch,
    getState=getState,
    ds18x20=ds18x20,
    onewire=onewire,
    dht=dht,
    ADC=ADC,
    Pin=Pin,
    gc=gc,
    time=time,
    requests=requests,
    datadog=datadog,
    logger=logger,
    watchdog=watchdog,
    machine=machine,
  )
  timer = Timer(0)
  timer.init(period=1000, mode=Timer.PERIODIC, callback=tick)

  # Start websocket server
  server.start()
  try:
    while True:
      server.process_all()
  except KeyboardInterrupt:
    pass

  server.stop()
