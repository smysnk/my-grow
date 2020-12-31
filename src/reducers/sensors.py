# Event Types
SENSOR_UPDATE_COMPLETE = 'SENSOR_UPDATE_COMPLETE'
SENSOR_UPDATE = 'SENSOR_UPDATE'

INSIDE_TENT = 'insideTent'
OUTSIDE_TENT = 'outsideTent'
FLOATER_BOTTOM = 'floaterBottom'
FLOATER_TOP = 'floaterTop'
RESERVOIR = 'reservoir'
PH = 'pH'
EMERGENCY_SHUTOFF = 'emergencyShutoff'

TEMPERATURE = 'temperature'
HUMIDITY = 'humidity'
STATE = 'state'
UPDATED_AT = 'updatedAt'
VALUE = 'value'
SENSOR = 'sensor'
PROPERTY = 'property'
TRIGGERED_RECENTLY = 'triggeredRecently'
TIME = 'time'
DEPTH = 'depth'

sensorsInitialState = {
  INSIDE_TENT: {
    TEMPERATURE: None,
    HUMIDITY: None,
    UPDATED_AT: None,
  },
  OUTSIDE_TENT: {
    TEMPERATURE: None,
    HUMIDITY: None,
    UPDATED_AT: None,
  },
  FLOATER_BOTTOM: {
    STATE: None,
    UPDATED_AT: None,
    TRIGGERED_RECENTLY: True,
  },
  FLOATER_TOP: {
    STATE: None,
    UPDATED_AT: None,
    TRIGGERED_RECENTLY: True,
  },
  EMERGENCY_SHUTOFF: {
    STATE: None,
    UPDATED_AT: None,
    TRIGGERED_RECENTLY: True,
  },
  RESERVOIR: {
    TEMPERATURE: None,
    UPDATED_AT: None,
    DEPTH: None,
  },
  PH: {
    VALUE: None,
    UPDATED_AT: None,
  },
}

class Sensors: 
  def __call__(self, state=sensorsInitialState, action={}):
    state = state.copy() # Ensure we're returning a new object
    sensor = action.get(SENSOR)
    prop = action.get(PROPERTY)

    if action.get('type') == SENSOR_UPDATE:
      state[sensor] = state[sensor].copy() # Ensure we're updating a new obj
      
      if state[sensor][prop] != action[VALUE]:
        state[sensor][prop] = action[VALUE]
        state[sensor][UPDATED_AT] = int(action[TIME])

    return state

