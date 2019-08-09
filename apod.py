import os
import requests
import random
from datetime import datetime
import pandas as pd
from flask import Flask, jsonify

app = Flask(__name__)

class Apod(object):

    def __init__(self, url=None, log_file=None, log_days_file=None):
        self.url = url
        self.log_file = log_file
        self.log_days_file = log_days_file

    def url(self):
        return self.url

    def log_file(self):
        return self.log_file

    def log_days_file(self):
        return self.log_days_file

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
            self.log_messages(message=message)
            self.log_days(date=date, title=title, link=apod_link)
        else:
            message = "APOD content isn't an image, generating random date to try again..."
            self.log_messages(message=message)
            self.log_days(date=date, title=title, link=apod_link)
            self.set_url_with_date("random")
            self.download_and_save_image()

    def random_date(self):
        already_downloaded = True
        while already_downloaded:
            start_date = datetime.today().replace(day=16, month=6, year=1995).toordinal()
            end_date = datetime.today().toordinal()
            date = datetime.fromordinal(random.randint(start_date, end_date)).strftime("%Y-%m-%d")
            already_downloaded = self.date_already_downloaded(date)
        return date

    def set_url_with_date(self, date=None):
        if not date is None:
            if date == "random":
                date = self.random_date()
        else:
            date = datetime.today().strftime("%Y-%m-%d")
        self.url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date={}".format(date)

    def date_already_downloaded(self, date):
        days_list = pd.read_csv(self.log_days_file, sep=";")
        days_list = days_list['date'].to_list()
        if date in days_list:
            return True
        return False

    def create_apod_directory(self):
        self.apod_directory = "{}/APOD/".format(os.path.expanduser("~"))
        if not os.path.exists(self.apod_directory):
            try:
                os.makedirs(self.apod_directory)
                self.log_messages(message="Creating directory {} to store images from APOD".format(self.apod_directory))
            except Exception as ex:
                self.log_messages(message="Error trying to create APOD directory: {}".format(ex))

    def log_messages(self, message):
        message = "{}: {}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message)
        with open(self.log_file, "a") as file:
            file.write("{}".format(message))

    def log_days(self, date, title, link):
        with open(self.log_days_file, "a") as file:
            file.write("{};{};{}\n".format(date, title, link))


@app.route("/healthcheck")
def healthcheck():
    return "it's alive!", 200

@app.route("/apod_wallpaper")
@app.route("/apod_wallpaper/<string:date>")
def apod_wallpaper(date=None):
    apod = Apod()
    try:
        apod.create_apod_directory()
        apod.log_file = "{}log.txt".format(apod.apod_directory)
        apod.log_days_file = "{}log_days.csv".format(apod.apod_directory)
        if (not os.path.isfile(apod.log_days_file)):
            with open(apod.log_days_file, 'w') as file:
                file.write('date;title;link\n')
        apod.set_url_with_date(date)
        apod.download_and_save_image(set_wallpaper=True)
        return "done", 200
    except Exception as ex:
        message = "Error: {}".format(ex)
        apod.log_messages(message=message)
        return message, 500

@app.route("/apod")
@app.route("/apod/<string:date>")
def apod(date=None):
    try:
        apod = Apod()
        apod.set_url_with_date(date)
        apod_data = jsonify(apod.get_apod_data())
        return apod_data, 200
    except Exception as ex:
        message = "Error: {}".format(ex)
        return message, 500

app.run()