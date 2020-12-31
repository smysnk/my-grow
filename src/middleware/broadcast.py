from ..reducers.sensors import SENSOR_UPDATE_COMPLETE
import json

def Broadcast(channel):
  def middleware(store):
    dispatch = store['dispatch']
    get_state = store['get_state']
    
    def apply_middleware(next):
      def apply_action(action):        
        if action is None:
          return action # Stop empty actions from going any further
        elif action.get('type') == SENSOR_UPDATE_COMPLETE:
          state = get_state()
          channel.broadcast(json.dumps(state))
          
        return next(action)        
      return apply_action
    return apply_middleware
  return middleware
