
SET_STATE = 'SET_STATE'

STATE_PUMP_BUCKET = 'STATE_PUMP_BUCKET'
STATE_PUMP_RESERVOIR = 'STATE_PUMP_RESERVOIR'
STATE_WAIT_BUCKET_EMPTY = 'STATE_WAIT_BUCKET_EMPTY'
STATE_WAIT_BUCKET_FULL = 'STATE_WAIT_BUCKET_FULL'

EMERGENCY_SHUTOFF = 'emergencyShutoff'
SET_EMERGENCY_SHUTOFF = 'SET_EMERGENCY_SHUTOFF'
UPDATED_AT = 'updatedAt'
STATE = 'state'

eventLoopInitialState = {
  STATE: None,
  "pumpBucket": {
    "startedAt": None,
    "endedAt": None,
    UPDATED_AT: None,
  },
  "pumpReservoir": {
    "startedAt": None,
    "endedAt": None,
    UPDATED_AT: None,
  },
  EMERGENCY_SHUTOFF: {
    STATE: False,
    UPDATED_AT: None,    
  }
}


class EventLoop: 
  # Defining __call__ method 
  def __call__(self, state=eventLoopInitialState, action={}):
    state = state.copy()

    if action.get('type') == STATE_PUMP_BUCKET:
      state['state'] = STATE_PUMP_BUCKET;
      state['pumpBucket'] = state['pumpBucket'].copy()
      state['pumpBucket'][UPDATED_AT] = action['time']
      if not state['pumpBucket']['startedAt']:
        state['pumpBucket']['startedAt'] = action['time']

    elif action.get('type') == STATE_PUMP_RESERVOIR:
      state['state'] = STATE_PUMP_RESERVOIR;
      state['pumpReservoir'] = state['pumpReservoir'].copy()
      state['pumpReservoir']['startedAt'] = action['time']
      if not state['pumpReservoir']['startedAt']:
        state['pumpBucket']['startedAt'] = action['time']
      
    elif action.get('type') == STATE_WAIT_BUCKET_EMPTY:
      state['state'] = STATE_WAIT_BUCKET_EMPTY;
      state['pumpBucket'] = state['pumpBucket'].copy()
      state['pumpBucket'][UPDATED_AT] = action['time']
      
    elif action.get('type') == STATE_WAIT_BUCKET_FULL:
      state['state'] = STATE_WAIT_BUCKET_FULL;
      state['pumpReservoir'] = state['pumpReservoir'].copy()
      state['pumpReservoir'][UPDATED_AT] = action['time']
      
    elif action.get('type') == SET_EMERGENCY_SHUTOFF:
      state['emergencyShutoff'][STATE] = action['value']
      return state
      
    return state
