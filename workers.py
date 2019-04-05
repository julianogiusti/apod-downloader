import os
import requests
import json

#TODO dados da imagem em um arquivo ou salvar no banco


class Worker(object):

    def __init__(self, date):
        self.url = os.environ['NASA_URL']+os.environ['NASA_API_KEY']

    def estabilish_connection_with_nasa(self):  
        h = requests.head(self.url, allow_redirects=True)
        header = h.headers
        content_type = header.get('content-type')
        if 'text' in content_type.lower():
            return False
        if 'html' in content_type.lower():
            return False
        return True

    def download_and_save_image(self, set_wallpaper=False):
        request = requests.get(self.url)
        info = json.loads(request.text)
        filename = info['hdurl'].split("/")[6]
        img = requests.get(info['hdurl'])
        if img.status_code == 200:
            file_path = '{}-{}-{}'.format(os.environ['MY_PATH_NASA_WALLPAPERS'], info['date'], filename)
            open(file_path, 'wb').write(img.content)
            return

        #if set_wallpaper:
        #   os.system("gsettings set org.gnome.desktop.background picture-uri file://{}".format(file_path))

date = ""
worker = Worker(date)

if worker.estabilish_connection_with_nasa():
    try:
        worker.download_and_save_image(set_wallpaper=False)
        print "APOD image downloaded successfully, enjoy!!"
    except Exception as ex:
        print "Oops, something went wrong, sorry about that :/"
        print "EXCEPTION: {}".format(ex)
print('Cant estabilish a connection with NASA')