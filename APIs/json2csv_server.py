import csv
import io

from flask import Flask, make_response, request

app = Flask(__name__)

__version__ = '1.0.0'


@app.route('/file/', methods=["POST"])
def post_file():
    text_file = io.StringIO()
    csv_file = csv.writer(text_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    try:
        received_json = request.get_json()
        if received_json:
            csv_file.writerow(received_json[0].keys())
        for dictionary in received_json:
            csv_file.writerow(dictionary.values())

    except Exception as error:
        return make_response(
            {'Bad format': f'{error}'},
            400,
        )
    else:
        response = make_response(text_file.getvalue())
        response.headers['Content-Disposition'] = 'attachment; filename=json2csv.csv'
        response.mimetype = 'text/csv'
        response.status_code = 200
        return response


@app.route('/version/', methods=["GET"])
def get_version():
    return __version__


if __name__ == '__main__':
    app.run(debug=True, port=5001)
