#!/usr/bin/env python3
import requests
import sys
import magic
import datetime
import pytz
import os
import json

starttime = datetime.datetime.utcnow()
configfile = open("config.json", "r")
config = json.loads(configfile.read())
configfile.close()

cwd = os.getcwd()
dest = config["dest"]
dictUrl = config["url"]
nztz = pytz.timezone(config["timezone"])

print("----------------------------------------------")
print(f"Webcamscraper started at {nztz.fromutc(starttime).strftime('%y%m%d-%H%M')}")

if nztz.fromutc(starttime).hour != int(config["hour"]):
    print("Closing due to wrong time")
else:
    successes = 0

    def getcam(dir, file):    
        minutesago = 0
        successful = False
        while minutesago < 30 and not successful:
            utc = starttime - datetime.timedelta(minutes=minutesago)
            time = nztz.fromutc(utc).strftime("%y%m%d-%H%M")
            url = f"{os.path.join(dir, file)}_{time}.jpg"
            print(f"Looking for image at {url}")
            myfile = requests.get(url)
            open(f"{os.path.join(cwd, file)}.jpg", "wb").write(myfile.content)
            if magic.from_file(f"{os.path.join(cwd, file)}.jpg", mime=True) == "image/jpeg":
                successful = True
            minutesago += 1

        if successful:
            print(f"Found valid jpg image for {file}.jpg")
            os.rename(f"{os.path.join(cwd, file)}.jpg", f"{os.path.join(dest, file)}.jpg")
            print(f"Moved {file}.jpg to {dest}")
            return True
        else:
            print(f"No jpg images found for {file}.jpg")
            return False

    for file, dir in dictUrl.items():
        if getcam(dir, file) == True:
            successes += 1

    print(f"webcamscraper found {successes} images in {(datetime.datetime.utcnow() - starttime).seconds} seconds")