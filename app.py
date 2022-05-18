from flask import Flask, render_template, request
import re
from flask import session, send_file

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secret key'
app.config["SESSION_TYPE"] = 'filesystem'

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
    option = request.form['options']
    print(option)
    if (option == "linux"):
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
            if ((i.split(" ")[0] + " " + i.split(" ")[1]) == "Move file"):
                name.append("mv " + (i.split(" ", 4)[2]) + " " + (i.split(" ", 4)[4]))
            if ((i.split(" ")[0] + " " + i.split(" ")[1]) == "Rename file"):
                name.append("mv " + (i.split(" ", 4)[2]) + " " + (i.split(" ", 4)[4]))
            if ((i.split(" ")[0] + " " + i.split(" ")[1]) == "Replace text"):
                name.append("sed -i 's/" + (i.split(" ", 7)[2]) + "/" + (i.split(" ", 7)[4]) + "/g'" + " " + (i.split(" ", 7)[7]))
            if ((i.split(" ")[0] + " " + i.split(" ")[1]) == "Delete empty"):
                name.append("sed -i '/^$/d'" + " " + i.split(" ", 4)[4])
            if ((i.split(" ")[0] + " " + i.split(" ")[1]) == "Print lines"):
                name.append("awk '/" + i.split(" ",5)[3] +"/ {print}' " + i.split(" ",5)[5])
        length = len(name)
        session['script'] = name
        session['os'] = option
        return render_template("index.html", name = name, length = length)
    else:
        for i in subcereri:
            if ((i.split(" ")[0] + " " +  i.split(" ")[1]) == "Create directory"):
                name.append("md " + (i.split(" at ",1)[1]))
            if ((i.split(" ")[0] + " " + i.split(" ")[1]) == "Create empty"):
                name.append("type nul > " + (i.split(" at ", 1)[1]))
            if ((i.split(" ")[0] + " " + i.split(" ")[1]) == "Delete directory"):
                name.append("rmdir /s" + (i.split(" from ", 1)[1]))
            if ((i.split(" ")[0] + " " + i.split(" ")[1]) == "Delete file"):
                name.append("del " + (i.split(" from ", 1)[1]))
            if ((i.split(" ")[0] + " " + i.split(" ")[1]) == "Move file"):
                name.append("move " + (i.split(" ", 4)[2]) + " " + (i.split(" ", 4)[4]))
            if ((i.split(" ")[0] + " " + i.split(" ")[1]) == "Rename file"):
                name.append("ren " + (i.split(" ", 4)[2]) + " " + (i.split(" ", 4)[4]))
            if ((i.split(" ")[0] + " " + i.split(" ")[1]) == "Replace text"):
                name.append("(gc " + (i.split(" ", 7)[7]) + ") " + "-replace " + "'" + (i.split(" ", 7)[2]) + "'" + ", " + "'"+ (i.split(" ", 7)[4]) + "'" +"|" + "Out-File " + (i.split(" ", 7)[7]))
            if ((i.split(" ")[0] + " " + i.split(" ")[1]) == "Delete empty"):
                name.append("(gc " + (i.split(" ",4)[4]) +") | ? {$_.trim() -ne ""} | set-content " + (i.split(" ",4)[4]))
            if ((i.split(" ")[0] + " " + i.split(" ")[1]) == "Print lines"):
                name.append("findstr " + i.split(" ", 5)[3] + " " + i.split(" ",5)[5])

        length = len(name)
        session['script'] = name
        session['os'] = option
        return render_template("index.html", name = name, length = length)

@app.route("/download", methods = ['POST', 'GET'])
def download():
    script_download = session.get('script', None)
    os_ales = session.get('os', None)
    length = len(script_download)
    if os_ales == "linux":
        file=open("script.txt", "w")
        file.write("#!/bin/bash" + "\n")
        for i in script_download:
            file.write(i + "\n")
        file.close()
        path = "E:\PythonProjects\script.txt"
        return send_file(path, as_attachment=True)
    else:
        file=open("script.txt", "w")
        for i in script_download:
            file.write(i + "\n")
        file.close()
        path = "E:\PythonProjects\script.txt"
        return send_file(path, as_attachment=True)

if __name__=='__main__':
    app.run(debug=True)