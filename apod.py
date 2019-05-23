import os
import sys
import requests
import random
from datetime import datetime

class Apod(object):

    def url(self):
        return self.url

    def apod_directory(self):
        return self.apod_directory

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
            message = "APOD image downloaded successfully, APOD web page: {}".format(apod_link)
            self.log_messages(message=message, apod_directory=self.apod_directory)
        else:
            message = "APOD content isn't an image, generating random date to try again..."
            self.log_messages(message=message, apod_directory=self.apod_directory)
            self.url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date={}".format(self.random_date())
            self.download_and_save_image()

    def random_date(self):
        start_date = datetime.today().replace(day=16, month=6, year=1995).toordinal()
        end_date = datetime.today().toordinal()
        date = datetime.fromordinal(random.randint(start_date, end_date)).strftime("%Y-%m-%d")
        return date

    def create_apod_directory(self):
        self.apod_directory = "{}/APOD/".format(os.path.expanduser("~"))
        if not os.path.exists(self.apod_directory):
            try:
                os.makedirs(self.apod_directory)
                self.log_messages(message="Creating directory {} to store images from APOD".format(self.apod_directory), apod_directory=self.apod_directory)
            except Exception as ex:
                self.log_messages(message="Error trying to create APOD directory: {}".format(ex), apod_directory=self.apod_directory)
                exit(1)

    def log_messages(self, message, apod_directory):
        log_file_path = "{}log.txt".format(apod_directory)
        message = "{}: {}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message)
        print message
        with open(log_file_path, "a") as file:
            file.write("{}".format(message))

apod = Apod()
apod.create_apod_directory()

if len(sys.argv) > 1:
    date = str(sys.argv[1])
    if date == "random":
        date = apod.random_date()
else:
    date = datetime.today().strftime("%Y-%m-%d")

apod.url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date={}".format(date)

try:
    apod.download_and_save_image(set_wallpaper=True)
except Exception as ex:
    message = "Oops, something went wrong, sorry about that :/ - Exception: {}".format(ex)
    apod.log_messages(message=message, apod_directory=apod.apod_directory)