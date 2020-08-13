#!/bin/python3
import requests
import magic
import datetime
import pytz
import os
import json

starttime = datetime.datetime.utcnow()
config = open("config.json", "r")
configObj = json.loads(config.read())
config.close()

log = open(configObj["log"], "a+")


def report(msg):
    print(msg)
    log.write(msg)


report("\n\n----------------------------------------------\n")

nztz = pytz.timezone("Pacific/Auckland")
tmpdir = configObj["tmpdir"]
finaldir = configObj["finaldir"]
dictUrl = configObj["url"]


def getcam(dir, file):

    def getimg(_dt):
        time = nztz.fromutc(_dt).strftime("%y%m%d-%H%M")
        fullUrl = f"{dir}{file}_{time}.jpg"
        report(f"\nLooking for image at {fullUrl}")
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
        report(f"\nFound valid jpg image for {file}.jpg")
        os.rename(f"{tmpdir}{file}.jpg", f"{finaldir}{file}.jpg")
        report(f"\nMoved {file}.jpg to {finaldir}")
    else:
        report(f"\nNo jpg images found for {file}.jpg")


for file, dir in dictUrl.items():
    getcam(dir, file)

log.close()
