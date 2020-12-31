from ..reducers.controls import CONTROL_MASK_SET, CONTROL_MASK_CLEAR, MASK, CONTROL_PORT_ON, CONTROL_PORT_OFF

def portsEnable(mask):
  return {
    'type': CONTROL_MASK_SET,
    MASK: mask
  }

def portsDisable(mask):
  return {
    'type': CONTROL_MASK_CLEAR,
    MASK: mask
  }

def portsOn(ports):
  return {
    'type': CONTROL_PORT_ON,
    'value': ports
  }

def portsOff(ports):
  return {
    'type': CONTROL_PORT_OFF,
    'value': ports
  }
