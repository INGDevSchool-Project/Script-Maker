from flask import Flask
app = Flask(__name__)

@app.route('/')
def get_car():
    return "Vruuum"

if __name__ == '__main__':
    app.run()