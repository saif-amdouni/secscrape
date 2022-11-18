from datetime import datetime

def standardized_timestamp(frequency, dt=None):

    if dt is None:
      dt = datetime.now() 

    frequency = int(frequency)
    # Special case were frequency=0 so we only return the date component
    if frequency == 0:
        return dt.strftime('%Y-%m-%d')

    blocks = 60 / frequency
    standardized_minutes = {}
    for block in range(blocks):
        standardized_minutes[block] = block * frequency

    collapsed_minutes = (dt.minute / frequency)
    minutes = standardized_minutes.get(collapsed_minutes, 0)
    timestamp = datetime(dt.year, dt.month, dt.day, dt.hour, minutes, 0)

    return timestamp.strftime('%Y%m%d%H%M%S')
