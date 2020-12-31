
class Series:
  def __init__(self):
    self.points = []

  def add(self, *args):
    for arg in args[:-1]:
      if arg is None:
        raise Exception('Keys should not contain invalid types')
    
    # Ignore empty datapoints
    if args[-1] is None:
      return
    
    self.points.append(('.'.join(args[:-1]), args[-1]))


class Agent:
  def __init__(self, requests=None, time=None, name=None, datadogApiKey=None, datadogApplicationKey=None, logger=None, timeout=2):
    self.time = time
    self.requests = requests
    self.name = name
    self.timeout = timeout
    self.headers = {
      "Content-Type": "application/json",
      "DD-API-KEY": datadogApiKey,
      "DD-APPLICATION-KEY": datadogApplicationKey,
    }
    self.log = logger(append='metrics:datadog')

  def submit(self, series):
    currentTime = self.time.time()
    seriesFormatted = []
    for point in series.points:
      seriesFormatted.append({
        "host": self.name,
        "metric": point[0],
        "points": [
          [
            currentTime + 946684800, # Number of seconds between unix (1970) and esp32 epoch (2000)
            point[1]
          ],
        ],
        "tags": [],
        "type": "gauge",
      })

    data = {
      "series": seriesFormatted,
    }

    response = None
    try:
      response = self.requests.post("https://api.datadoghq.com/api/v1/series", headers=self.headers, json=data, timeout=self.timeout)
      json = response.json()
      if json['status'] == 'ok':
        self.log("Metrics submitted", name='periodic')
        pass
    except OSError as e:
      self.log("Failed submitting metrics", e, name='periodic')

    if response:
      response.close()
