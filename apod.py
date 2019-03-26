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


    def get_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


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
        date = self.__request_result.json()['date']
        media_type = self.__request_result.json()['media_type']
        title = self.__request_result.json()['title']
        apod_link = "https://apod.nasa.gov/apod/ap{}.html".format(date.replace("-", "")[2:])

        if media_type == "image":
            hdurl = self.__request_result.json()['hdurl']
            self.__image = requests.get(hdurl, allow_redirects=True)

            filename = title.replace(" ", "_")
            image_path = '/home/juliano/Pictures/APOD/{}-{}'.format(date, filename)
            open(image_path, 'wb').write(self.__image.content)
            status = "downloaded"
            if set_wallpaper:
                os.system("gsettings set org.gnome.desktop.background picture-uri file://{}".format(image_path))
        else:
            status = "not_downloaded"
        self.log_links(date, apod_link, media_type, status)


    def log_links(self, date, link, type, status):
        image_list_path = "/home/juliano/Pictures/APOD/images_list.csv"
        colnames = ['date', 'link', 'type', 'status']
        if (not os.path.isfile(image_list_path )):
            with open(image_list_path , 'a') as file:
                file.write(';'.join(map(str, colnames)))
                file.write('\n')
        row_content = "{};{};{};{}\n".format(date, link, type, status)
        with open(image_list_path, "a") as file:
            file.write(row_content)


    def log_messages(self, message):
        log_file_path = "/home/juliano/Pictures/APOD/log.txt"
        with open(log_file_path, "a") as file:
            file.write("{}: {}\n".format(self.get_time(), message))



# date in format yyyy-mm-dd: 2019-01-01
date = ""
apod = Apod(date)
apod.log_messages("Script started execution")
print "Script started execution"

apod.get_apod_data()

if apod.is_downloadable():
    try:
        apod.download_and_save_image(set_wallpaper=True)
        message = "APOD image downloaded successfully"
        print message
        apod.log_messages(message)
    except Exception as ex:
        message = "Oops, something went wrong, sorry about that :/ - Exception: {}".format(ex)
        print message
        apod.log_messages(message)
else:
    message = "Sorry, can't download file. Probably, the cause is that today at apod there is a video file, which this script still not handle, maybe in the future, who knows."
    apod.log_messages(message)
    print message

apod.log_messages("Script finished execution")
print "Script finished execution"
