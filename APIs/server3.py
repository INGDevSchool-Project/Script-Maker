from flask import Flask, jsonify, make_response

app = Flask(__name__)

cars = {
    '1':{
        'car-type' : '4 Wheel Drive',
        'brand' : 'ARO',
        'color' : ['white', 'metal gray', 'blue cosmos', 'army green']
    }
}