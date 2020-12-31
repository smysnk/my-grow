import network, ntptime, machine, env, time
import lib.timew

sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
  print('connecting to network...')
  sta_if.active(True)
  sta_if.config(dhcp_hostname=env.settings['controllerName'])
  sta_if.connect(env.settings['wifiAP'], env.settings['wifiPassword'])
  while not sta_if.isconnected():
    pass

  # Get current time from internets
  ntptime.settime()
