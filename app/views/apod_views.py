from http import HTTPStatus

from flask import make_response, render_template, request

from app.services.apod_services import Apod
from app import app


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/healthcheck')
def healthcheck():
    return make_response({'data': {}, 'message': "It's alive!"}, HTTPStatus.OK)


@app.route('/apod_wallpaper')
def apod_wallpaper():
    date = request.args.get('date', None)
    apod = Apod()
    try:
        apod.download_and_set_wallpaper(date=date)
        return 'done', 200
    except Exception as ex:
        message = f'Error: {ex}'
        apod.log_messages(message=message)
        return message, 500


@app.route('/apod')
def apod():
    date = request.args.get('date', None)
    apod = Apod()
    try:
        apod.set_url_with_date(date)
        apod_data = apod.get_apod_data()
        return make_response(
            {'data': apod_data, 'message': 'ok'}, HTTPStatus.OK
        )
    except Exception as ex:
        return make_response(
            {'data': {}, 'message': f'Error: {ex}'},
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
