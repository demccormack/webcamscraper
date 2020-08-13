#!/bin/python3
import requests
import magic
import datetime
import pytz
import os
import json

starttime = datetime.datetime.utcnow() - datetime.timedelta(hours=3)
config = open("config.json", "r")
configObj = json.loads(config.read())
config.close()

log = open(configObj["log"], "a+")


def report(msg):
    print(msg)
    log.write(f"\n{msg}")


report("\n----------------------------------------------")

nztz = pytz.timezone("Pacific/Auckland")
tmpdir = configObj["tmpdir"]
finaldir = configObj["finaldir"]
dictUrl = configObj["url"]
successes = 0

def getcam(dir, file):
    
    def getimg(_dt):
        time = nztz.fromutc(_dt).strftime("%y%m%d-%H%M")
        fullUrl = f"{dir}{file}_{time}.jpg"
        report(f"Looking for image at {fullUrl}")
        myfile = requests.get(fullUrl)
        open(f"{tmpdir}{file}.jpg", "wb").write(myfile.content)
        
    dt = starttime
    getimg(dt)

    onemin = datetime.timedelta(minutes=1)
    loops = 0
    successful = False
    while loops < 29 and not successful:
        dt = dt - onemin
        getimg(dt)
        loops += 1
        if magic.from_file(f"{tmpdir}{file}.jpg", mime=True) == "image/jpeg":
            successful = True

    if successful:
        report(f"Found valid jpg image for {file}.jpg")
        os.rename(f"{tmpdir}{file}.jpg", f"{finaldir}{file}.jpg")
        successes += 1
        report(f"Moved {file}.jpg to {finaldir}")
    else:
        report(f"No jpg images found for {file}.jpg")


for file, dir in dictUrl.items():
    getcam(dir, file)

report(f"webcamscraper found {successes} images in {datetime.datetime.utcnow() - starttime}")
log.close()