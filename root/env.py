settings = {
  'wifiAP': '',
  'wifiPassword': '',
  'controllerName': 'my-grow',
  'settingWaitBucketFull': 60 * 3, # seconds
  'settingWaitBucketEmpty': 60 * 20, # seconds
  'settingWaitDecoupleFloater': 30, # Seconds to wait after a floater change (Allows time for fluids to equalize in system before attemting to pump them again)
  'settingOverEmpty': 20, # Seconds to continue pumping after the bucket is empty
  'settingOverFill': 5, # Seconds to continue pumping after the bucket is full
  'datadogApiKey': '',
  'datadogApplicationKey': '',
  'datadogInterval': 10, # seconds,
  'debug': True,
  'logInclude': ['.*'], # regex
  'logExclude': ['reservoir:depth$', ':periodic$'], # regex
  'watchdog': True,
  'httpTimeout': 2, # seconds

  # Auto-Updating
  'githubRemote': 'https://github.com/smysnk/my-grow',
  'githubUsername': '',
  'githubToken': '',
}
