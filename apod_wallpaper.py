from app.services.apod_services import Apod


def run_apod_wallpaper(date=None):
    apod = Apod()
    apod.download_and_set_wallpaper(date=date)


if __name__ == '__main__':
    run_apod_wallpaper()
