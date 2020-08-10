#!/bin/python3
import requests
import magic
import datetime
import pytz
import os
import json

starttime = datetime.datetime.utcnow()# - datetime.timedelta(hours=8) # for debugging outside webcam operating hours
config = open("config.json", "r")
configObj = json.loads(config.read())
config.close()

log = open(configObj["log"], "a+")


def report(msg):
    print(msg)
    log.write(msg)


report("\n\n----------------------------------------------\n")

nztz = pytz.timezone("Pacific/Auckland")
tmpTarget = configObj["tmpTarget"] + "{}"
finalTarget = configObj["finalTarget"] + "{}"
dictUrl = configObj["url"]


def getCam(url, target):

    def getImg(_dt):
        strTime = nztz.fromutc(_dt).strftime("%y%m%d-%H%M")
        fullUrl = url.format(t=strTime)
        report("\nLooking for image at " + fullUrl)
        myfile = requests.get(fullUrl)
        open(tmpTarget.format(target), "wb").write(myfile.content)

    dt = starttime
    getImg(dt)

    onemin = datetime.timedelta(minutes=1)
    loops = 0
    while loops < 29 and magic.from_file(tmpTarget.format(target), mime=True) == "application/octet-stream":
        dt = dt - onemin
        getImg(dt)
        loops += 1

    if magic.from_file(tmpTarget.format(target), mime=True) == "image/jpeg":
        report("\nFound valid jpg image for {}".format(target))
        os.rename(tmpTarget.format(target), finalTarget.format(target))
        report("\nMoved {} to live web folder".format(target))
    else:
        report("\nNo jpg images found for {}".format(target))


for key in dictUrl:
    getCam("{dir}{file}_{t}.jpg".format(
        dir=dictUrl[key], file=key, t="{t}"), "{}.jpg".format(key))

log.close()
