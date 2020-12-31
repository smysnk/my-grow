from ..reducers.sensors import SENSOR_UPDATE, TEMPERATURE, HUMIDITY, STATE, SENSOR, PROPERTY, VALUE, RESERVOIR, TIME, DEPTH


class DS18X20():
  def __init__(self, ds18x20=None, onewire=None, pin=None, dispatch=None, name="Untitled", time=None):
    self.probe = ds18x20.DS18X20(onewire.OneWire(pin))
    self.name = name
    self.dispatch = dispatch
    self.onewire = onewire
    self.time = time

  def measure(self):
    roms = self.probe.scan()
    try:
      self.probe.convert_temp()
    except self.onewire.OneWireError:
      return

    try:
      for rom in roms:
        self.dispatch({
          "type": SENSOR_UPDATE,
          SENSOR: self.name,
          PROPERTY: TEMPERATURE,
          VALUE: self.probe.read_temp(rom),
          TIME: self.time.time(),
        })
    except Exception as e:
      print(e)


class Dht():
  def __init__(self, dht=None, pin=None, dispatch=None, name="Untitled", time=None):
    self.sensor = dht.DHT22(pin)
    self.name = name
    self.dispatch = dispatch
    self.time = time

  def measure(self):
    self.sensor.measure()

    self.dispatch({
      "type": SENSOR_UPDATE,
      SENSOR: self.name,
      PROPERTY: TEMPERATURE,
      VALUE: self.sensor.temperature(),
      TIME: self.time.time(),
    })

    self.dispatch({
      "type": SENSOR_UPDATE,
      SENSOR: self.name,
      PROPERTY: HUMIDITY,
      VALUE: self.sensor.humidity(),
      TIME: self.time.time(),
    })

class Switch():
  def __init__(self, Pin=None, pin=None, dispatch=None, name="Untitled", time=None):
    self.pin = pin
    self.dispatch = dispatch
    self.name = name
    self.time = time

  def measure(self):
    self.dispatch({
      "type": SENSOR_UPDATE,
      SENSOR: self.name,
      PROPERTY: STATE,
      VALUE: self.pin.value(),
      TIME: self.time.time(),
    })

class A2D():
  def __init__(self, pin=None, ADC=None, dispatch=None, name="Untitled", time=None):
    self.adc = ADC(pin)
    self.adc.atten(ADC.ATTN_11DB) # 0 - 3.6V range
    self.name = name
    self.dispatch = dispatch
    self.time = time

  def measure(self):
    self.dispatch({
      "type": SENSOR_UPDATE,
      SENSOR: self.name,
      PROPERTY: VALUE,
      VALUE: self.adc.read(),
      TIME: self.time.time(),
    })

class TimeoutWaitingSteadyState(Exception): pass
class TimeoutMeasurement(Exception): pass

class HCSR04:
  def __init__(self, trigger=None, echo=None, echo_timeout_us=500*2*30, time=None, machine=None, dispatch=None, name='Untitled'):
    self.echo_timeout_us = echo_timeout_us
    self.machine = machine
    self.time = time
    self.name = name
    self.dispatch = dispatch
    
    self.trigger = trigger
    self.echo = echo

    self.trigger.value(0)


  def _send_pulse_and_wait(self):
    self.trigger.value(0) # Stabilize the sensor
    self.time.sleep_us(5)
    self.trigger.value(1)
    # Send a 10us pulse.
    self.time.sleep_us(10)
    self.trigger.value(0)

    pulse_time = self.machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
    if pulse_time == -1: raise TimeoutMeasurement()
    if pulse_time == -2: raise TimeoutWaitingSteadyState()
    return pulse_time

  def measure(self):
    pulse_time = self._send_pulse_and_wait()    
    distance = (pulse_time / 2) / 29.1
    self.dispatch({
      "type": SENSOR_UPDATE,
      SENSOR: self.name,
      PROPERTY: DEPTH,
      VALUE: 34.5 - distance,
      TIME: self.time.time(),
    })
