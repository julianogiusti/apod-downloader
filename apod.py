import os
import sys
import requests
import random
from datetime import datetime
from flask import Flask, jsonify

app = Flask(__name__)

class Apod(object):

    def url(self):
        return self.url

    def apod_directory(self):
        return self.apod_directory

    def get_apod_data(self):
        response = requests.get(self.url).json()
        return response

    def download_and_save_image(self, set_wallpaper=False):
        request_response = self.get_apod_data()
        date = request_response['date']
        media_type = request_response['media_type']
        title = request_response['title']
        apod_link = "https://apod.nasa.gov/apod/ap{}.html".format(date.replace("-", "")[2:])

        if media_type == "image":
            hdurl = request_response['hdurl']
            image = requests.get(hdurl, allow_redirects=True)

            filename = title.replace(" ", "_")
            file_extension = hdurl.split("/")[-1].split(".")[-1]
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


@app.route("/healthcheck")
def healthcheck():
    return "it's alive!", 200

@app.route("/apod_wallpaper")
@app.route("/apod_wallpaper/<string:date>")
def apod_wallpaper(date=None):
    apod = Apod()
    apod.create_apod_directory()

    if not date is None:
        if date == "random":
            date = apod.random_date()
    else:
        date = datetime.today().strftime("%Y-%m-%d")
    apod.url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date={}".format(date)
    try:
        apod.download_and_save_image(set_wallpaper=True)
        return "done", 200
    except Exception as ex:
        message = "Oops, something went wrong, sorry about that :/ - Exception: {}".format(ex)
        apod.log_messages(message=message, apod_directory=apod.apod_directory)
        return message, 500

@app.route("/apod")
@app.route("/apod/<string:date>")
def apod(date=None):
    apod = Apod()
    if not date is None:
        if date == "random":
            date = apod.random_date()
    else:
        date = datetime.today().strftime("%Y-%m-%d")
    apod.url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date={}".format(date)
    try:
        apod_data = jsonify(apod.get_apod_data())
        return apod_data, 200
    except Exception as ex:
        message = "Oops, something went wrong, sorry about that :/ - Exception: {}".format(ex)
        return message, 500

app.run()