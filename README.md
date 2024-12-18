# APOD downloader
A simple script/API to download the [NASA's Astronomy Picture of the Day](https://apod.nasa.gov).

This script was written using Python and Flask to download the picture and set it as wallpapers on ubuntu 18.04 with gnome.

## Using it
Install requirements:

    $ pip install -r requirements.txt

Run the Flask app:

    $ python run.py

You can now call the API in http://127.0.0.1:5000/apod, choosing a date or "random" to get one date from 1995-06-16 to today:

    $ curl -X GET "http://127.0.0.1:5000/apod?date=2019-05-21"
    $ curl -X GET "http://127.0.0.1:5000/apod?date=random"

If you don't choose a date, the current day is chosen by default.

    $ curl -X GET http://127.0.0.1:5000/apod

To use the functionality to download and set wallpaper on Ubuntu, you can use the /apod_wallpaper endpoint:

    $ curl -X GET http://127.0.0.1:5000/apod_wallpaper
    $ curl -X GET "http://127.0.0.1:5000/apod_wallpaper?date=2019-05-21"
    $ curl -X GET "http://127.0.0.1:5000/apod_wallpaper?date=random"

## References and sources:
- [Downloading files from URLs in Python](https://www.codementor.io/aviaryan/downloading-files-from-urls-in-python-77q3bs0un)
- [Nasa Open APIs](https://api.nasa.gov/)
