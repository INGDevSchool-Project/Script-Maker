from flask import Flask, jsonify, make_response

app = Flask(__name__)


@app.route('/', methods=["GET"])
def get_car():
    response = make_response(
        jsonify({
            'car-type':'4 Wheel Drive',
            'brand':'ARO',
            'color':['white','metal grey', 'blue cosmos', 'army green']
        }),
        200,
    )
    return response

if __name__ == '__main__':
    app.run(debug=True)

