from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

cars = {}


@app.route('/car/<car_id>/', methods=["GET"])
def get_car(car_id):
    if cars.get(car_id):
        message = jsonify(cars[car_id])
        status_code = 200
    else:
        message = {'message': 'not found'}
        status_code = 404
    return make_response(
        message,
        status_code,
    )


@app.route('/cars/', methods=["POST"])
def post_cars():
    global cars
    cars.update(request.get_json())
    return make_response(
        {'message': 'updated'},
        200,
    )


if __name__ == '__main__':
    app.run(debug=True)
