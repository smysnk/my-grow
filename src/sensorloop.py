from .reducers import sensors
from .reducers import controls
from .reducers import eventloop
from .reducers import runtime
from . import lib
from . import actions

def setup(
  dispatch=None,
  getState=None,
  ds18x20=None,
  onewire=None,
  dht=None,
  ADC=None,
  Pin=None,
  gc=None,
  time=None,
  datadog=None,
  requests=None,
  logger=None,
  watchdog=None,
  machine=None,
  updater=None,
):

  log = logger('sensorloop')
  state = getState()
  # Used to track when to send metrics to datadog
  agent = None
  if state['runtime'][runtime.DATADOG_INTERVAL]:
    agent = datadog.Agent(
      time=time,
      name=state['runtime'][runtime.CONTROLLER_NAME],
      requests=requests,
      datadogApiKey=state['runtime'][runtime.DATADOG_API_KEY],
      datadogApplicationKey=state['runtime'][runtime.DATADOG_APPLICATION_KEY],
      logger=logger,
      timeout=state['runtime'][runtime.HTTP_TIMEOUT],
    )

  # Wire up sensors
  pin = Pin(13, Pin.IN, Pin.PULL_DOWN)
  floatBottom = lib.sensors.Switch(Pin=Pin, pin=pin, dispatch=dispatch, name=sensors.FLOATER_BOTTOM, time=time)
  floatBottomActions = actions.sensors.Switch(pin=pin, name=sensors.FLOATER_BOTTOM, time=time)

  pin = Pin(14, Pin.IN, Pin.PULL_DOWN)
  floatTop = lib.sensors.Switch(Pin=Pin, pin=pin, dispatch=dispatch, name=sensors.FLOATER_TOP, time=time)
  floatTopActions = actions.sensors.Switch(pin=pin, name=sensors.FLOATER_TOP, time=time)

  pin = Pin(12, Pin.IN, Pin.PULL_DOWN)
  emergencyShutoff = lib.sensors.Switch(Pin=Pin, pin=pin, dispatch=dispatch, name=sensors.EMERGENCY_SHUTOFF, time=time)
  emergencyShutoffActions = actions.sensors.Switch(pin=pin, name=sensors.EMERGENCY_SHUTOFF, time=time)

  pin = Pin(22)
  insideTent = lib.sensors.Dht(dht=dht, pin=pin, dispatch=dispatch, name=sensors.INSIDE_TENT, time=time)

  pin = Pin(23)
  outsideTent = lib.sensors.Dht(dht=dht, pin=pin, dispatch=dispatch, name=sensors.OUTSIDE_TENT, time=time)

  pin = Pin(32)
  reservoir = lib.sensors.DS18X20(ds18x20=ds18x20, onewire=onewire, pin=pin, dispatch=dispatch, name=sensors.RESERVOIR, time=time)

  pin = Pin(36)
  pH = lib.sensors.A2D(pin=pin, ADC=ADC, dispatch=dispatch, name=sensors.PH, time=time)

  pinTrigger = Pin(5, mode=Pin.OUT, pull=None)
  pinEcho = Pin(34, mode=Pin.IN, pull=None)
  reservoirDepth = lib.sensors.HCSR04(trigger=pinTrigger, echo=pinEcho, time=time, machine=machine, name=sensors.RESERVOIR, dispatch=dispatch)

  _sensors = [insideTent, outsideTent, reservoir, pH, reservoirDepth, floatTop, floatBottom, emergencyShutoff]

  def tick(_):

    for sensor in _sensors:
      try:
        sensor.measure()
      except lib.sensors.TimeoutWaitingSteadyState as e:
        log('Timeout waiting for sensor steady state', name='sensor:reservoir:depth')
      except lib.sensors.TimeoutMeasurement as e:
        log('Timeout waiting for measurement', name='sensor:reservoir:depth')
      except OSError as e:
        log(e, name='sensor')

    state = getState()
    # If water hits the top of the bucket, trigger an emergency shutoff
    if state['sensors'][sensors.EMERGENCY_SHUTOFF][sensors.STATE]:
      # dispatch(actions.controls.portsDisable(controls.PORT_PUMP_BUCKET | controls.PORT_PUMP_RESERVOIR))
      dispatch(actions.eventloop.emergencyShutoff(True))

    dispatch(actions.runtime.update(gc=gc, time=time))
    dispatch(actions.sensors.updateComplete())

    state = getState()
    if not state['eventloop']['state']:
      # Start the system pumping the bucket out
      dispatch(actions.eventloop.startPumpingReservoir(time.time()))
      log('Transitioning to [STATE_PUMP_RESERVOIR] state')

    elif state['eventloop']['state'] == eventloop.STATE_WAIT_BUCKET_EMPTY:
      # Waiting to see if the bucket system is empty
      
      # Turn off the pump so the bucket because there is no more water in there
      if time.time() - state['eventloop']['pumpBucket'][eventloop.UPDATED_AT] > state['runtime'][runtime.SETTING_OVER_EMPTY] and state['controls'][controls.PINS] & controls.PORT_PUMP_BUCKET == 1:
        dispatch(actions.controls.portsOff(controls.PORT_PUMP_BUCKET))
        log('Turning off [PORT_PUMP_BUCKET]')

      # If the water has remained high for enough time
      if time.time() - state['eventloop']['pumpBucket'][eventloop.UPDATED_AT] > state['runtime'][runtime.SETTING_WAIT_BUCKET_EMPTY]:
        dispatch(actions.eventloop.startPumpingReservoir(time.time()))
        log('Transitioning to [STATE_PUMP_RESERVOIR] state')

      # If the bottom floater goes up, we still need to pump some more
      if time.time() - state['eventloop']['pumpBucket'][eventloop.UPDATED_AT] > state['runtime'][runtime.SETTING_WAIT_DECOUPLE_FLOATER] and state['sensors'][sensors.FLOATER_BOTTOM][sensors.STATE]:
        dispatch(actions.eventloop.startPumpingBucket(time.time()))
        log('Transitioning to [STATE_PUMP_BUCKET] state')

    elif state['eventloop']['state'] == eventloop.STATE_PUMP_BUCKET:
      # While pumping out of bucket

      if state['controls'][controls.PINS] & controls.PORT_PUMP_BUCKET == 0:
        dispatch(actions.controls.portsOn(controls.PORT_PUMP_BUCKET))      
        log('Turning on [PORT_PUMP_BUCKET]')

      if not state['sensors'][sensors.FLOATER_BOTTOM][sensors.STATE]:
        # If bucket is empty, lets wait a bit
        dispatch(actions.eventloop.waitBucketEmpty(time.time()))
        log('Transitioning to [STATE_WAIT_BUCKET_EMPTY] state')

    elif state['eventloop']['state'] == eventloop.STATE_WAIT_BUCKET_FULL:
      # Waiting to see if the bucket system is full

      if time.time() - state['eventloop']['pumpReservoir'][eventloop.UPDATED_AT] > state['runtime'][runtime.SETTING_OVER_FILL] and (state['controls'][controls.PINS] & controls.PORT_PUMP_RESERVOIR) >> 1 == 1:
        # Turn off the pump so the bucket doesn't overflow
        dispatch(actions.controls.portsOff(controls.PORT_PUMP_RESERVOIR))
        log('Turning off [PORT_PUMP_RESERVOIR]')

      # If the water has remained high for enough time
      if time.time() - state['eventloop']['pumpReservoir'][eventloop.UPDATED_AT] > state['runtime'][runtime.SETTING_WAIT_BUCKET_FULL]:
        dispatch(actions.eventloop.startPumpingBucket(time.time()))
        log('Transitioning to [STATE_PUMP_BUCKET] state')
        
      # If the top floater goes low, need to pump more into bucket
      if time.time() - state['eventloop']['pumpReservoir'][eventloop.UPDATED_AT] > state['runtime'][runtime.SETTING_WAIT_DECOUPLE_FLOATER] and not state['sensors'][sensors.FLOATER_TOP][sensors.STATE]:
        dispatch(actions.eventloop.startPumpingReservoir(time.time()))
        log('Transitioning to [STATE_PUMP_RESERVOIR] state')

    elif state['eventloop']['state'] == eventloop.STATE_PUMP_RESERVOIR:
      # Pumping water from reservoir into bucket

      if (state['controls'][controls.PINS] & controls.PORT_PUMP_RESERVOIR) >> 1 == 0:
        dispatch(actions.controls.portsOn(controls.PORT_PUMP_RESERVOIR))
        log('Turning on [PORT_PUMP_RESERVOIR]')
        
      if state['sensors'][sensors.FLOATER_TOP][sensors.STATE]:
        # If bucket is full, lets wait a bit
        dispatch(actions.eventloop.waitBucketFull(time.time()))
        log('Transitioning to [STATE_WAIT_BUCKET_FULL] state')

    # Submit datadog metrics every 10 seconds
    state = getState()
    if state['runtime'][runtime.DATADOG_INTERVAL] and time.time() % state['runtime'][runtime.DATADOG_INTERVAL] == 0:
      series = datadog.Series()
      series.add('sensors', sensors.FLOATER_TOP, sensors.STATE, state['sensors'][sensors.FLOATER_TOP][sensors.STATE])
      series.add('sensors', sensors.FLOATER_TOP, sensors.UPDATED_AT, state['sensors'][sensors.FLOATER_TOP][sensors.UPDATED_AT])
      series.add('sensors', sensors.FLOATER_BOTTOM, sensors.STATE, state['sensors'][sensors.FLOATER_BOTTOM][sensors.STATE])
      series.add('sensors', sensors.FLOATER_BOTTOM, sensors.UPDATED_AT, state['sensors'][sensors.FLOATER_BOTTOM][sensors.UPDATED_AT])
      series.add('sensors', sensors.EMERGENCY_SHUTOFF, sensors.STATE, state['sensors'][sensors.EMERGENCY_SHUTOFF][sensors.STATE])
      series.add('sensors', sensors.EMERGENCY_SHUTOFF, sensors.UPDATED_AT, state['sensors'][sensors.EMERGENCY_SHUTOFF][sensors.UPDATED_AT])
      series.add('sensors', sensors.INSIDE_TENT, sensors.TEMPERATURE, state['sensors'][sensors.INSIDE_TENT][sensors.TEMPERATURE])
      series.add('sensors', sensors.INSIDE_TENT, sensors.HUMIDITY, state['sensors'][sensors.INSIDE_TENT][sensors.HUMIDITY])
      series.add('sensors', sensors.INSIDE_TENT, sensors.UPDATED_AT, state['sensors'][sensors.INSIDE_TENT][sensors.UPDATED_AT])
      series.add('sensors', sensors.OUTSIDE_TENT, sensors.TEMPERATURE, state['sensors'][sensors.OUTSIDE_TENT][sensors.TEMPERATURE])
      series.add('sensors', sensors.OUTSIDE_TENT, sensors.HUMIDITY, state['sensors'][sensors.OUTSIDE_TENT][sensors.HUMIDITY])
      series.add('sensors', sensors.OUTSIDE_TENT, sensors.UPDATED_AT, state['sensors'][sensors.OUTSIDE_TENT][sensors.UPDATED_AT])
      series.add('sensors', sensors.RESERVOIR, sensors.TEMPERATURE, state['sensors'][sensors.RESERVOIR][sensors.TEMPERATURE])
      series.add('sensors', sensors.RESERVOIR, sensors.UPDATED_AT, state['sensors'][sensors.RESERVOIR][sensors.UPDATED_AT])
      series.add('sensors', sensors.RESERVOIR, sensors.DEPTH, state['sensors'][sensors.RESERVOIR][sensors.DEPTH])
      series.add('sensors', sensors.PH, sensors.VALUE, state['sensors'][sensors.PH][sensors.VALUE])
      series.add('sensors', sensors.PH, sensors.UPDATED_AT, state['sensors'][sensors.PH][sensors.UPDATED_AT])
      series.add('runtime', runtime.CURRENT_TIME, state['runtime'][runtime.CURRENT_TIME])
      series.add('runtime', runtime.UPTIME, state['runtime'][runtime.UPTIME])
      series.add('runtime', runtime.MEMORY_FREE, state['runtime'][runtime.MEMORY_FREE])
      series.add('runtime', runtime.MEMORY_ALLOCATED, state['runtime'][runtime.MEMORY_ALLOCATED])
      series.add('runtime', runtime.SETTING_WAIT_BUCKET_FULL, state['runtime'][runtime.SETTING_WAIT_BUCKET_FULL])
      series.add('runtime', runtime.SETTING_WAIT_BUCKET_EMPTY, state['runtime'][runtime.SETTING_WAIT_BUCKET_EMPTY])
      series.add('runtime', runtime.DATADOG_INTERVAL, state['runtime'][runtime.DATADOG_INTERVAL])
      series.add('controls', 'port', 'pump_bucket', (state['controls'][controls.PINS] & controls.PORT_PUMP_BUCKET) >> 0)
      series.add('controls', 'port', 'pump_reservoir',(state['controls'][controls.PINS] & controls.PORT_PUMP_RESERVOIR) >> 1)
      series.add('controls', 'port', 'lights', (state['controls'][controls.PINS] & controls.PORT_LIGHTS) >> 2)
      series.add('controls', 'port', 'aux', (state['controls'][controls.PINS] & controls.PORT_AUX) >> 3)
      series.add('controls', 'mask', 'pump_bucket', (state['controls'][controls.MASK] & controls.PORT_PUMP_BUCKET) >> 0)
      series.add('controls', 'mask', 'pump_reservoir',(state['controls'][controls.MASK] & controls.PORT_PUMP_RESERVOIR) >> 1)
      series.add('controls', 'mask', 'lights', (state['controls'][controls.MASK] & controls.PORT_LIGHTS) >> 2)
      series.add('controls', 'mask', 'aux', (state['controls'][controls.MASK] & controls.PORT_AUX) >> 3)

      # Enumerate current state of event loop
      enum = [eventloop.STATE_PUMP_BUCKET, eventloop.STATE_PUMP_RESERVOIR, eventloop.STATE_WAIT_BUCKET_EMPTY, eventloop.STATE_WAIT_BUCKET_FULL]
      elState = -1
      try:
        elState = enum.index(state['eventloop']['state'])
      except ValueError:
        pass

      series.add('eventloop', 'state', elState)
      series.add('eventloop', eventloop.EMERGENCY_SHUTOFF, eventloop.STATE, state['eventloop'][eventloop.EMERGENCY_SHUTOFF][eventloop.STATE])
      series.add('eventloop', eventloop.EMERGENCY_SHUTOFF, eventloop.UPDATED_AT, state['eventloop'][eventloop.EMERGENCY_SHUTOFF][eventloop.UPDATED_AT])

      agent.submit(series)

    # Reset the device if an update is available
    if state['runtime'][runtime.OTA_AUTO_UPDATE_INTERVAL] and time.time() % state['runtime'][runtime.OTA_AUTO_UPDATE_INTERVAL] == 0:
      try:
        updater.checkForUpdate()
      except Exception as e:
        log('Failed to check for OTA update:', e)

    # Feed the watchdog so the system doesn't reset
    if watchdog:
      watchdog.feed()
    
    log('tick', name='periodic')

  return tick
