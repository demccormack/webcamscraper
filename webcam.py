#!/usr/bin/env python3
import requests
import magic
import datetime
import pytz
import os
import json

starttime = datetime.datetime.utcnow() - datetime.timedelta(hours=3)
configfile = open("config.json", "r")
config = json.loads(configfile.read())
configfile.close()


def report(msg):
    print(msg)
    log = open(config["log"], "a+")
    log.write(f"\n{msg}")
    log.close()


report("\n----------------------------------------------")

nztz = pytz.timezone("Pacific/Auckland")
tmpdir = config["tmpdir"]
finaldir = config["finaldir"]
dictUrl = config["url"]
successes = 0

def getcam(dir, file):    
    minutesago = 0
    successful = False
    while minutesago < 30 and not successful:
        utc = starttime - datetime.timedelta(minutes=minutesago)
        time = nztz.fromutc(utc).strftime("%y%m%d-%H%M")
        url = f"{dir}{file}_{time}.jpg"
        report(f"Looking for image at {url}")
        myfile = requests.get(url)
        open(f"{tmpdir}{file}.jpg", "wb").write(myfile.content)
        if magic.from_file(f"{tmpdir}{file}.jpg", mime=True) == "image/jpeg":
            successful = True
        minutesago += 1

    if successful:
        report(f"Found valid jpg image for {file}.jpg")
        os.rename(f"{tmpdir}{file}.jpg", f"{finaldir}{file}.jpg")
        report(f"Moved {file}.jpg to {finaldir}")
        return True
    else:
        report(f"No jpg images found for {file}.jpg")
        return False

for file, dir in dictUrl.items():
    if getcam(dir, file) == True:
        successes += 1

report(f"webcamscraper found {successes} images in {(datetime.datetime.utcnow() - starttime).seconds} seconds")