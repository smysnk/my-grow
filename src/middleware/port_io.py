from ..reducers.controls import MASK, PINS, PORT_PUMP_BUCKET, PORT_PUMP_RESERVOIR, PORT_LIGHTS, PORT_AUX
from ..reducers import eventloop

class PortIO:
  def __init__(self, Pin=None, logger=None):
    self.pins = [
      { 'io': Pin(27, Pin.OUT), 'bit': PORT_PUMP_BUCKET },
      { 'io': Pin(25, Pin.OUT), 'bit': PORT_PUMP_RESERVOIR },
      { 'io': Pin(26, Pin.OUT), 'bit': PORT_LIGHTS },
      { 'io': Pin(33, Pin.OUT), 'bit': PORT_AUX },
    ]
    
    self.emergencyIndicator = Pin(2, Pin.OUT)
    self.logger = logger

  def getInit(self):
    def init(store):
      dispatch = store['dispatch']
      get_state = store['get_state']

      def apply_middleware(next):
        def apply_action(action):
          
          if action is None:
            return action # Stop empty actions from going any further
          elif callable(action): # Functions have __name__, dicts do not
            result = action(dispatch, get_state, self.logger) # Thunk It
          else:
            result = next(action)

          state = get_state()
          self.emergencyIndicator.value(state['eventloop'][eventloop.EMERGENCY_SHUTOFF][eventloop.STATE])

          if result.get('type').startswith('CONTROL') or result.get('type') == 'STARTUP':
            for n in range(len(self.pins)):
            
              # Apply whole pin pask
              value = state['controls'][PINS] & state['controls'][MASK]

              # Mask only that bit and shift to get specific pin value
              value = (value & self.pins[n]['bit']) >> n
              
              # Inverse because relays use inverse logic
              value = 0 if value == 1 else 1

              self.pins[n]['io'].value(value)
          
          return result

        return apply_action
      return apply_middleware
    return init