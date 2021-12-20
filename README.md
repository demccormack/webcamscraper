Webcam image URLs often contain the time when the image was taken. If the images are not taken at regular times, it is difficult to access them programmatically. This script looks for the latest image and then copies it to our own static URL for easier access. It does this daily.

The script can take up to two minutes depending on connection speed, so it should be scheduled to run automatically in the background, e.g. using cron. Detecting the time in Python instead of cron means I can allow for daylight saving clock changes.

To use the script, create a ```config.json``` file in the same directory using the following format:

```
{
    "timezone" : "Pacific/Auckland",
    "hour" : "8",
    "dest" : "/var/www/",
    "url" : {
        "name1.jpg": "https://some-url.com/webcam/name1/name1_%y%m%d-%H%M.jpg",
        "name2.jpg": "https://some-url.com/webcam/name2/name1_%y%m%d-%H%M.jpg"
    },
    "debug": {
        "enabled": "Debug is on. Make this string empty to disable debugging.",
        "forceHour": "8",
        "forceMinute": "15"
    }
}
```

The ```url``` array can contain as many images as you like. Only jpeg images are supported. Replace any date/time 
components in the URL with the substitutions given in 
[Python strftime() documentation](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes).

The example config would produce the following output:

```
Looking for image at https://some-url.com/webcam/name1/name1_200815-0854.jpg
Looking for image at https://some-url.com/webcam/name1/name1_200815-0853.jpg
Looking for image at https://some-url.com/webcam/name1/name1_200815-0852.jpg
Looking for image at https://some-url.com/webcam/name1/name1_200815-0851.jpg
Found valid jpg image for name1.jpg
Moved name1.jpg to /var/www/
Looking for image at https://some-url.com/webcam/name2/name2_200815-0854.jpg
Looking for image at https://some-url.com/webcam/name2/name2_200815-0853.jpg
Looking for image at https://some-url.com/webcam/name2/name2_200815-0852.jpg
Looking for image at https://some-url.com/webcam/name2/name2_200815-0851.jpg
Looking for image at https://some-url.com/webcam/name2/name2_200815-0850.jpg
Found valid jpg image for name2.jpg
Moved name2.jpg to /var/www/
webcamscraper found 2 images in 16 seconds
```

Finally, set up a cron job to run the script at 15 minutes past the hour by adding the following line to ```/etc/crontab``` (replace ```user``` with your Linux username):
```
15 * * * * user cd ~/webcamscraper && python3 webcamscraper.py >> webcamscraper.log
```