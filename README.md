Webcam image URLs often contain the time when the image was taken. If the images 
are not taken at regular times, it is difficult to access them programmatically. 
This script looks for the latest image and then copies it to our own static URL 
for easier access. The script is quite slow (up to a minute), but it can be scheduled 
to run automatically in the background, e.g. using cron.

To use the script, create a file called config.json in the same directory using 
the following format (note that the trailing slashes are required in all but the 
first parameter):

```
{
    "log" : "~/webcamscraper/log",
    "tmpdir" : "~/webcamscraper/",
    "finaldir" : "/var/www/",
    "url" : {"name1": "https://some-url.com/webcam/name1/",
         "name2": "https://some-url.com/webcam/name2/"}
}
```

If you are using Windows, replace all forward slashes / in log, tmpdir and finaldir 
with two backslashes \\\\

The url array can contain as many images as you like. Only jpeg images with names ending 
in ".jpg" are supported, but don't add this suffix to any of the parameters in the config 
file.