from ..reducers.sensors import SENSOR_UPDATE, TEMPERATURE, HUMIDITY, STATE, SENSOR, PROPERTY, VALUE, SENSOR_UPDATE_COMPLETE, TIME

def updateComplete():
  return {
    'type': SENSOR_UPDATE_COMPLETE,
  }

class Switch:

  def __init__(self, pin=None, name=None, time=None):
    self.name = name
    self.pin = pin
    self.time = time

  def updateState(self, name=None, previousState=None):
    state = bool(self.pin.value())
    if state == previousState:
      return None

    return {
      'type': SENSOR_UPDATE,
      SENSOR: name if name is not None else self.name,
      PROPERTY: STATE,
      VALUE: state,
      TIME: self.time.time(),
    }

