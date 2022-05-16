from flask import Flask
app = Flask(__name__)

@app.route('/test/')
def get_car():
    return "Vruuum"

if __name__ == '__main__':
    app.run()

