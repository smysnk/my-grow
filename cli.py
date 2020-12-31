import os, json, itertools, sys
from datadog import initialize, api
from src.env import settings
from more_itertools import first_true

template = None
with open('./dd/grow_dashboard.json') as f:
  template = json.load(f)

options = {
  'api_key': settings['datadogApiKey'],
  'app_key': settings['datadogApplicationKey'],
}

initialize(**options)

results = api.Dashboard.get_all()
dashboard = first_true(results['dashboards'], pred=lambda x:  x['title'] == template['title'])

if not dashboard:
  print("Create dashboard")
  template.pop('id', None)
  results = api.Dashboard.create(**template)
else:
  print("Updating dashboard [%s]" % dashboard['id'])
  template['id'] = dashboard['id']
  results = api.Dashboard.update(**template)

print("Dashboard url: https://app.datadoghq.com%s" % results['url'])