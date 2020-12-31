SET_BOOT_TIMESTAMP = 'SET_BOOT_TIMESTAMP'
UPDATE = 'UPDATE'

BOOT_TIMESTAMP = 'bootTimestamp'
UPTIME = 'uptime'
MEMORY_FREE = 'memoryFree'
MEMORY_ALLOCATED = 'memoryAllocated'
CURRENT_TIME = 'currentTime'
CURRENT_TIME_FORMATTED = 'currentTimeFormatted'
SETTING_WAIT_BUCKET_FULL = 'settingWaitBucketFull'
SETTING_WAIT_BUCKET_EMPTY = 'settingWaitBucketEmpty'
SETTING_WAIT_DECOUPLE_FLOATER = 'settingWaitDecoupleFloater'
SETTING_OVER_EMPTY = 'settingOverEmpty'
SETTING_OVER_FILL = 'settingOverFill'
CONTROLLER_NAME = 'controllerName'
DATADOG_API_KEY = 'datadogApiKey'
DATADOG_APPLICATION_KEY = 'datadogApplicationKey'
DATADOG_INTERVAL = 'datadogInterval'
DEBUG = 'debug'
LOG_INCLUDE = 'logInclude'
LOG_EXCLUDE = 'logExclude'
HTTP_TIMEOUT = 'httpTimeout'

class Runtime: 
  def __init__(self, env=None):
    self.initialState = {
      BOOT_TIMESTAMP: None,
      UPTIME: None,
      MEMORY_FREE: None,
      MEMORY_ALLOCATED: None,
      CURRENT_TIME: None,
      CURRENT_TIME_FORMATTED: None,
      SETTING_WAIT_BUCKET_FULL: env.settings[SETTING_WAIT_BUCKET_FULL],
      SETTING_WAIT_BUCKET_EMPTY: env.settings[SETTING_WAIT_BUCKET_EMPTY],
      SETTING_WAIT_DECOUPLE_FLOATER: env.settings[SETTING_WAIT_DECOUPLE_FLOATER],
      SETTING_OVER_FILL: env.settings[SETTING_OVER_FILL],
      SETTING_OVER_EMPTY: env.settings[SETTING_OVER_EMPTY],
      CONTROLLER_NAME: env.settings[CONTROLLER_NAME],
      DATADOG_API_KEY: env.settings[DATADOG_API_KEY],
      DATADOG_APPLICATION_KEY: env.settings[DATADOG_APPLICATION_KEY],
      DATADOG_INTERVAL: env.settings[DATADOG_INTERVAL],
      DEBUG: env.settings[DEBUG],
      LOG_INCLUDE: env.settings[LOG_INCLUDE],
      LOG_EXCLUDE: env.settings[LOG_EXCLUDE],
      HTTP_TIMEOUT: env.settings[HTTP_TIMEOUT],
    }

  def __call__(self, state=None, action={}):
    state = self.initialState if not state else state
    state = state.copy()
    if action.get('type') == SET_BOOT_TIMESTAMP:
      state['bootTimestamp'] = action['value']
      return state
    elif action.get('type') == UPDATE:
      state['currentTime'] = action['currentTime']
      state['currentTimeFormatted'] = action['currentTimeFormatted']
      state['uptime'] = action['currentTime'] - state['bootTimestamp']
      state['memoryFree'] = action['memoryFree']
      state['memoryAllocated'] = action['memoryAllocated']
      return state
    else:
      return state
