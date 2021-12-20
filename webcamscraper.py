#!/usr/bin/env python3
import requests
import sys
import magic
import datetime
from datetime import timedelta
from datetime import datetime
import pytz
import os
import json

configfile = open("config.json", "r")
config = json.loads(configfile.read())
configfile.close()

dest = config["dest"]
localtz = pytz.timezone(config["timezone"])

def getLocalTime():
    localtime = localtz.fromutc(datetime.utcnow())
    if config["debug"]["enabled"]:
        h = int(config["debug"]["forceHour"])
        m = int(config["debug"]["forceMinute"])
        localtime -= timedelta(hours=(localtime.hour - h), minutes=(localtime.minute - m))
        if localtime > localtz.fromutc(datetime.utcnow()):
            localtime -= timedelta(days=1)
    return localtime

localstarttime = getLocalTime()

print("----------------------------------------------")
if config["debug"]["enabled"]:
    print(f"Debug enabled. Simulating running at {localstarttime.strftime('%Y%m%d_%H%M')}")
else:
    print(f"Webcamscraper started at {localstarttime.strftime('%Y%m%d_%H%M')}")

if localstarttime.hour != int(config["hour"]) and not config["debug"]["enabled"]:
    print("Closing due to wrong time")
else:
    successes = 0

    def getcam(cam):
        name = cam["name"]
        url = cam["url"]
        mimetype = cam["mimetype"]
        myfile = None
        minutesago = 0
        successful = False

        while minutesago < 60 and not successful:
            trytime = localstarttime - timedelta(minutes=minutesago)
            tryurl = trytime.strftime(url)
            print(f"Looking for image at {tryurl}")
            myfile = requests.get(tryurl)
            if magic.from_buffer(myfile.content, mime=True) == mimetype:
                successful = True
            minutesago += 1

        if successful:
            print(f"Found valid {mimetype.split('/')[-1]} file for {name}")
            open(os.path.join(dest, name), "wb").write(myfile.content)
            print(f"Wrote {name} to {dest}")
        else:
            print(f"No {mimetype.split('/')[-1]} files found for {name}")
        
        return successful

    for cam in config["webcams"]:
        successes += getcam(cam)

    localfinishtime = getLocalTime()
    timetaken = (localfinishtime - localstarttime).seconds
    print(f"webcamscraper found {successes} images in {timetaken} seconds")

    if successes < len(config["webcams"]):
        exit(1)