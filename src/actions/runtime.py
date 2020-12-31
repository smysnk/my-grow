from ..reducers.runtime import UPDATE

def update(gc=None, time=None):
  days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

  # Sat, 19 Dec 2020 20:05:00 GMT
  t = time.localtime()  
  timestamp = "%s, %d %s %d %02d:%02d:%02d GMT" % (days[t[6]], t[2], month[t[1]-1], t[0], t[3], t[4], t[5])

  gc.collect()

  return {
    'type': UPDATE,
    'currentTime': time.time(), 
    'currentTimeFormatted': timestamp,
    'memoryFree': gc.mem_free(),
    'memoryAllocated': gc.mem_alloc(),
  }