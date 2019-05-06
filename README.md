# APOD downloader
A simple script to download the [NASA's Astronomy Picture of the Day](https://apod.nasa.gov).
This script was written using Python 2.7 to download the picture and set it as wallpapers on ubuntu 18.04 with gnome.

## Using it
Install requirements:

    $ pip install -r requirements.txt

Run the script:

    $ python apod.py <date>

You can choose the date as an argument usind the format ```yyyy-mm-dd```:

    $ python apod.py 2019-05-04

If you don't choose a date, the current day is chosen by default.

## References and sources:
- [Downloading files from URLs in Python](https://www.codementor.io/aviaryan/downloading-files-from-urls-in-python-77q3bs0un)
- [Nasa Open APIs](https://api.nasa.gov/)
