
CONTROL_MASK_SET = 'CONTROL_MASK_SET'
CONTROL_MASK_CLEAR = 'CONTROL_MASK_CLEAR'
CONTROL_PORT_ON = 'CONTROL_PORT_ON'
CONTROL_PORT_OFF = 'CONTROL_PORT_OFF'
PINS = 'PINS'
MASK = 'MASK'

PORT_PUMP_BUCKET = 1
PORT_PUMP_RESERVOIR = 2
PORT_LIGHTS = 4
PORT_AUX = 8

controlsInitialState = {
  PINS: 0,
  MASK: PORT_PUMP_BUCKET | PORT_PUMP_RESERVOIR | PORT_LIGHTS | PORT_AUX,
}

class Controls: 
  def __call__(self, state=controlsInitialState, action={}):
    state = state.copy()
    if action.get('type') == CONTROL_PORT_ON:
      state[PINS] = state[PINS] | action['value']

    elif action.get('type') == CONTROL_PORT_OFF:
      state[PINS] = state[PINS] & ~action['value']

    elif action.get('type') == CONTROL_MASK_SET:
      state[MASK] = state[MASK] | action[MASK]

    elif action.get('type') == CONTROL_MASK_CLEAR:
      state[MASK] = state[MASK] & ~action[MASK]

    return state