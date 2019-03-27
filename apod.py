# -*- coding: utf-8 -*-
import os
import re
import requests
from datetime import datetime

def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log_links(date, link, type, apod_directory):
    image_list_path = "{}images_list.csv".format(apod_directory)
    colnames = ['date', 'link', 'type']
    if (not os.path.isfile(image_list_path )):
        with open(image_list_path , 'a') as file:
            file.write(';'.join(map(str, colnames)))
            file.write('\n')
    row_content = "{};{};{}\n".format(date, link, type)
    with open(image_list_path, "a") as file:
        file.write(row_content)


def log_messages(message, apod_directory):
    log_file_path = "{}log.txt".format(apod_directory)
    message = "{}: {}\n".format(get_time(), message)
    print message
    with open(log_file_path, "a") as file:
        file.write("{}".format(message))


class Apod(object):

    def __init__(self, date, apod_directory):
        self.url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date={}".format(date)
        self.apod_directory = apod_directory


    def download_and_save_image(self, set_wallpaper=False):
        request_result = requests.get(self.url)
        date = request_result.json()['date']
        media_type = request_result.json()['media_type']
        title = request_result.json()['title']
        apod_link = "https://apod.nasa.gov/apod/ap{}.html".format(date.replace("-", "")[2:])

        if media_type == "image":
            hdurl = request_result.json()['hdurl']
            image = requests.get(hdurl, allow_redirects=True)

            filename = title.replace(" ", "_")
            file_extension = hdurl.split("/")[6].split(".")[1]
            image_path = '{}{}-{}.{}'.format(self.apod_directory, date, filename, file_extension)
            wallpaper_path = '{}wallpaper.{}'.format(self.apod_directory, file_extension)
            open(image_path, 'wb').write(image.content)
            open(wallpaper_path, 'wb').write(image.content)
            if set_wallpaper:
                os.system("gsettings set org.gnome.desktop.background picture-uri file://{}".format(wallpaper_path))
            message = "APOD image downloaded successfully"
            log_messages(message=message, apod_directory=self.apod_directory)
        else:
            message = "APOD content isn't an image, so it's not being downloaded"
            log_messages(message=message, apod_directory=self.apod_directory)
        log_links(date=date, link=apod_link, type=media_type, apod_directory=self.apod_directory)

date = datetime.now().strftime("%Y-%m-%d")
apod_directory = "{}/APOD/".format(os.path.expanduser("~"))
if not os.path.exists(apod_directory):
    try:
        os.makedirs(apod_directory)
        log_messages(message="Creating directory {} to store images from APOD".format(apod_directory), apod_directory=apod_directory)
    except Exception as ex:
        log_messages(message="Error trying to create APOD directory: {}".format(ex), apod_directory=apod_directory)
        exit(1)
log_messages(message="Script started execution", apod_directory=apod_directory)
apod = Apod(date, apod_directory)
try:
    apod.download_and_save_image(set_wallpaper=True)
except Exception as ex:
    message = "Oops, something went wrong, sorry about that :/ - Exception: {}".format(ex)
    log_messages(message=message, apod_directory=apod_directory)
log_messages("Script finished execution", apod_directory=apod_directory)