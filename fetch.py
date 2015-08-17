#!/usr/bin/env python3
# coding: utf-8

import urllib.request
from datetime import datetime, timedelta
import csv
import sys
import json
import codecs

GROUP_MAPPING = dict({
"2. Liga Herren":           "H2L",
"3. Liga Herren Gruppe I":  "H3L",
"3. Liga Herren Gruppe II": "H3L",
"4. Liga Herren Gruppe I":  "H4L",
"4. Liga Herren Gruppe II": "H4L",
"2. Liga Damen":            "D2L",
"3. Liga Damen Gruppe I":   "D3L",
"3. Liga Damen Gruppe II":  "D3L",
"3. Liga Pro Damen":        "D3Lpro",
"4. Liga Damen Gruppe I":   "D4L",
"4. Liga Damen Gruppe II":  "D4L",
"5. Liga Damen Gruppe I":   "D5L",
"5. Liga Damen Gruppe II":  "D5L",
"5. Liga Damen Gruppe III": "D5L",
"Damen U23 1":              "DU23/1",
"Damen U23 2":              "DU23/2",
"Damen U23 3":              "DU23/3",
"Damen U19 1":              "DU19/1",
"Damen U19 2":              "DU19/2",
"Damen U17 1":              "DU17/1",
"Damen U17 2":              "DU17/2",
"Damen U23 2 Gruppe I":     "DU23/1",
"Damen U23 2 Gruppe II":    "DU23/2",
"Damen U19 2 Gruppe I":     "DU19/1",
"Damen U19 2 Gruppe II":    "DU19/2",
"Damen U17 2 Gruppe I":     "DU17/1",
"Damen U17 2 Gruppe II":    "DU17/2",
"Seniorinnen":              "SEN"
})

HEADER = ['StartDate', 'StartTime', 'EndDate', 'EndTime', 'Location', 'Subject']

def to_unicode(value):
    try:
        try:
            return unicode(value, "ascii")
        except UnicodeError:
            return unicode(value, "utf-8")
    except TypeError:
        return value.encode('utf-8')

if __name__ == '__main__':
    local_filename, headers = urllib.request.urlretrieve(sys.argv[1])
    print(local_filename)
    data = json.load(open(local_filename, 'r'))
    groups = dict()
    for game in data.get('results', dict()).get('games', dict()):
        try:
            start_time = datetime.strptime(game.get('datetime').split('\n')[0], "%d.%m.%y %H:%M")
            end_time = start_time + timedelta(hours=1, minutes=30)
            location = game.get('location').split('\n')[1]
            group = game.get('group')
            home = game.get('home')
            guest = game.get('guest')
            row = []
            row.append(start_time.strftime("%Y-%m-%d"))
            row.append(start_time.strftime("%H:%M"))
            row.append(end_time.strftime("%Y-%m-%d"))
            row.append(end_time.strftime("%H:%M"))
            row.append(location)
            row.append(GROUP_MAPPING.get(group, "VBCS") + ": {0} - {1}".format(home, guest))
            groups.setdefault(group, []).append(row)
        except ValueError:
            pass
    if True:
        for key, value in groups.items():
            filename = GROUP_MAPPING.get(key, "VBCS").replace('/', '_') + ".csv"
            print('writing {0}'.format(filename))
            fd = codecs.open(filename, 'w', encoding='utf-8')
            writer = csv.writer(fd, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(HEADER)
            for row in value:
                writer.writerow(row)
            fd.close()
