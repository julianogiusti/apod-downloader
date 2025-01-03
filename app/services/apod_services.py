import os
import random
from datetime import datetime

import pandas as pd
import requests


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
        apod_link = (
            f'https://apod.nasa.gov/apod/ap{date.replace("-", "")[2:]}.html'
        )

        if media_type == 'image':
            hdurl = request_response['hdurl']
            image = requests.get(hdurl, allow_redirects=True)

            filename = title.replace(' ', '_')
            filename = filename.replace('/', '_')
            file_extension = hdurl.split('/')[-1].split('.')[-1]
            image_path = (
                f'{self.apod_directory}{date}-{filename}.{file_extension}'
            )
            wallpaper_path = f'{self.apod_directory}wallpaper.{file_extension}'
            open(image_path, 'wb').write(image.content)
            open(wallpaper_path, 'wb').write(image.content)
            if set_wallpaper:
                # para gnome 42, precisa checar se está no tema 'dark', se estiver, precisa ajustar conforme abaixo
                # os.system(f'gsettings set org.gnome.desktop.background picture-uri-dark file://{wallpaper_path}')
                # [[ `gsettings get org.gnome.desktop.interface color-scheme` =~ 'dark' ]] && echo dark mode active || echo dark mode inactive
                os.system(
                    f'gsettings set org.gnome.desktop.background picture-uri-dark file://{wallpaper_path}'
                )
            message = f'APOD image downloaded successfully, APOD web page: {apod_link}'
            self.log_messages(message=message)
            self.log_days(date=date, title=title, link=apod_link)
        else:
            message = "APOD content isn't an image, generating random date to try again..."
            self.log_messages(message=message)
            self.log_days(date=date, title=title, link=apod_link)
            self.set_url_with_date('random')
            self.download_and_save_image()

    def download_and_set_wallpaper(self, date=None):
        self.create_apod_directory()
        self.log_file = f'{self.apod_directory}log.txt'
        self.log_days_file = f'{self.apod_directory}log_days.csv'
        if not os.path.isfile(self.log_days_file):
            with open(self.log_days_file, 'w') as file:
                file.write('date;title;link\n')
        self.set_url_with_date(date=date)
        self.download_and_save_image(set_wallpaper=True)

    def random_date(self):
        already_downloaded = True
        while already_downloaded:
            start_date = (
                datetime.today()
                .replace(day=16, month=6, year=1995)
                .toordinal()
            )
            end_date = datetime.today().toordinal()
            date = datetime.fromordinal(
                random.randint(start_date, end_date)
            ).strftime('%Y-%m-%d')
            already_downloaded = self.date_already_downloaded(date)
        return date

    def set_url_with_date(self, date=None):
        if date is None:
            date = datetime.today().strftime('%Y-%m-%d')

        if date == 'random':
            date = self.random_date()

        self.url = (
            f'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date={date}'
        )

    def date_already_downloaded(self, date):
        days_list = pd.read_csv(self.log_days_file, sep=';')
        days_list = days_list['date'].to_list()
        if date in days_list:
            return True
        return False

    def create_apod_directory(self):
        self.apod_directory = f'{os.path.expanduser("~")}/APOD/'
        if not os.path.exists(self.apod_directory):
            try:
                os.makedirs(self.apod_directory)
                self.log_messages(
                    message=f'Creating directory {self.apod_directory} to store images from APOD'
                )
            except Exception as ex:
                self.log_messages(
                    message=f'Error trying to create APOD directory: {ex}'
                )

    def log_messages(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f'{timestamp}: {message}\n'
        with open(self.log_file, 'a') as file:
            file.write(f'{message}')

    def log_days(self, date, title, link):
        with open(self.log_days_file, 'a') as file:
            file.write(f'{date};{title};{link}\n')
