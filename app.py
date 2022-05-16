from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route("/")

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/result", methods = ['POST', 'GET'])
def result():
    output = request.form.to_dict()
    count = 0
    cerere = output["name"]
    for i in cerere:
        if i == ';':
            count = count+1
    subcereri = cerere.split(";",count)
    name=[]
    for i in subcereri:
        ## Pentru model cu comenzi in baza de date
        ## Pentru fiecare comanda, cererea o sa arate intr-un anumit fel
        ## Ex: Create a directory: Create directory at [path]/[directory name]
        ## In baza de date putem avea o coloana cu comanda in sine si un identificator, spre ex. primele 2 cuvinte din cerere
        ## Codu de mai jos o sa se schimbe intr-un name.append(*interogare baza de date pe baza primelor 2 cuvinte din cerere* + ...)
        ## Poate o sa mai fie un if sau poate mai multe, s-ar putea sa fie niste cazuri speciale
        if ((i.split(" ")[0] + " " +  i.split(" ")[1]) == "Create directory"):
            name.append("mkdir " + (i.split(" at ",1)[1]))
        if ((i.split(" ")[0] + " " + i.split(" ")[1]) == "Create empty"):
            name.append("touch " + (i.split(" at ", 1)[1]))
        if ((i.split(" ")[0] + " " + i.split(" ")[1]) == "Delete directory"):
            name.append("rmdir " + (i.split(" from ", 1)[1]))
        if ((i.split(" ")[0] + " " + i.split(" ")[1]) == "Delete file"):
            name.append("rm " + (i.split(" from ", 1)[1]))

    length = len(name)
    return render_template("index.html", name = name, length = length)
if __name__=='__main__':
    app.run(debug=True)