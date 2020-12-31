import update, env, lib.requests, lib.logger, lib.requests, lib.timew, time, os, machine
from lib import base64

t = lib.timew.Time(time=time)

# Configure Logger
logger = lib.logger.config(enabled=env.settings['debug'], include=env.settings['logInclude'], exclude=env.settings['logExclude'], time=t)
log = logger(append='boot')
log("The current time is %s" % t.human())

logger = logger(append='OTAUpdater')

io = update.IO(os=os, logger=logger)
github = update.GitHub(
  io=io,
  remote=env.settings['githubRemote'],
  branch='master',
  logger=logger,
  requests=lib.requests,
  username=env.settings['githubUsername'],
  token=env.settings['githubToken'],
  base64=base64,
)
updater = update.OTAUpdater(io=io, github=github, logger=logger, machine=machine)

try:
  updater.update()
except Exception as e:
  log('Failed to OTA update:', e)

try:
  import src.main
  src.main.start(env=env, requests=lib.requests, logger=logger, time=t, updater=updater)
except:
  print('Failed to start.')
