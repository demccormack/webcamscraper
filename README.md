Webcam image URLs often contain the time when the image was taken. If the images 
are not taken at regular times, it is difficult to access them programmatically. 
This script looks for the latest image and then copies it to our own static URL 
for easier access. The script is quite slow (up to two minutes depending on connection speed), but it can be scheduled to run automatically in the background, e.g. using cron. This branch detects the time and exits unless it is between 8am and 9am. Detecting the time in Python instead of Cron means I can allow for daylight saving clock changes.

To use the script, create a file called config.json in the same directory using 
the following format:

```
{
    "timezone" : "Pacific/Auckland",
    "hour" : "8",
    "dest" : "/var/www/",
    "url" : {"name1": "https://some-url.com/webcam/name1/",
         "name2": "https://some-url.com/webcam/name2/"}
}
```

The ```url``` array can contain as many images as you like. Only jpeg images with names ending 
in ```.jpg``` are supported, but don't add this suffix to any of the parameters in the config 
file.

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

Finally, set up a cron job to run the script every hour.