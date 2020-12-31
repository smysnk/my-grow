

class Agent():
  series = []
  def __init__(self, urequests, time):
    self.time = time
    self.urequests = urequests
    self.headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": "",
        "DD-APPLICATION-KEY": ""
    }

  def add(self, measurement):
    currentTime = self.time.time() + 946684800
    self.series.append({
      "host": "test.example.com",
      "interval": 20,
      "metric": "esp32." + measurement["name"],
      "points": [
        [
          currentTime,
          measurement["temperature"]
        ]
      ],
      "tags": [
        "environment:test"
      ],
      "type": "gauge"
    })

  def submit(self):

    print("submitting..")

    data = {
      "series": self.series
    }

    response = self.urequests.post("https://api.datadoghq.com/api/v1/series", headers=self.headers, json=data)
    response.close()

  def clear(self):
    self.series = []
