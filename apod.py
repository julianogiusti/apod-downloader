# -*- coding: utf-8 -*-
import os
import re
import requests
from datetime import datetime

class Apod(object):
    __request_result = ""
    __image = ""

    def __init__(self, date):
        self.url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
        self.date = date


    def get_date(self):
        return datetime.now().strftime("%Y-%m-%d")


    def is_downloadable(self):
        """
        Does the url contain a downloadable resource
        """
        h = requests.head(self.url, allow_redirects=True)
        header = h.headers
        content_type = header.get('content-type')
        if 'text' in content_type.lower():
            return False
        if 'html' in content_type.lower():
            return False
        return True


    def get_filename_from_cd(self, cd):
        """
        Get filename from content-disposition
        """
        if not cd:
            return None
        fname = re.findall('filename=(.+)', cd)
        if len(fname) == 0:
            return None
        return fname[0]


    def get_apod_data(self):
        if not apod.date == "":
            self.__request_result = requests.get("{}&date={}".format(self.url, date))
        else:
            self.__request_result = requests.get(self.url)


    def download_and_save_image(self, set_wallpaper=False):
        self.__image = requests.get(self.__request_result.json()['hdurl'], allow_redirects=True)
        filename = self.__request_result.json()['hdurl'].split("/")[6]
        if self.date != "":
            date = self.date
        else:
            date = self.get_date()
        file_path = '/home/juliano/Pictures/APOD/{}-{}'.format(date, filename)
        open(file_path, 'wb').write(self.__image.content)
        if set_wallpaper:
            os.system("gsettings set org.gnome.desktop.background picture-uri file://{}".format(file_path))


# date in format yyyy-mm-dd: 2019-01-01
date = ""
apod = Apod(date)
apod.get_apod_data()

if apod.is_downloadable():
    try:
        apod.download_and_save_image(set_wallpaper=True)
        print "APOD image downloaded successfully, enjoy!!"
    except Exception as ex:
        print "Oops, something went wrong, sorry about that :/"
        print "EXCEPTION: {}".format(ex)
else:
    print "Sorry, can't download file.\nProbably, the cause is that today at apod there is a video file, which this script still not handle, maybe in the future, who knows."
