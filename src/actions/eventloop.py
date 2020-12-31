from ..reducers import eventloop

def setState(state):
  return {
    'type': eventloop.SET_STATE,
    'state': state
  }

def startPumpingBucket(time=None):
  return {
    'type': eventloop.STATE_PUMP_BUCKET,
    'time': time,
  }

def startPumpingReservoir(time=None):
  return {
    'type': eventloop.STATE_PUMP_RESERVOIR,
    'time': time,
  }

def waitBucketFull(time=None):
  return {
    'type': eventloop.STATE_WAIT_BUCKET_FULL,
    'time': time,
  }

def waitBucketEmpty(time=None):
  return {
    'type': eventloop.STATE_WAIT_BUCKET_EMPTY,
    'time': time,
  }

def emergencyShutoff(value):
  return {
    'type': eventloop.SET_EMERGENCY_SHUTOFF,
    'value': value,
  }
