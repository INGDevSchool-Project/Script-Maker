from flask import Flask, render_template, request
from sqlalchemy import create_engine, select, MetaData, Table, and_
import re
import os
from flask import session, send_file,flash,redirect, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secret key'
app.config["SESSION_TYPE"] = 'filesystem'

engine = create_engine("mysql+mysqldb://public:password@localhost:3306/scripts", echo=True, future=True)
conn = engine.connect()


metadata = MetaData(bind=None)
table = Table(
    'commands',
    metadata,
    autoload=True,
    autoload_with=engine
)

stmt = select([
    table.columns.idcommand,
    table.columns.input,
    table.columns.linux,
    table.columns.windows,
    table.columns.youtube,
])

connection = engine.connect()
tables = connection.execute(stmt).fetchall()


@app.route("/")

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/result", methods = ['POST', 'GET'])
def result():
    output = request.form.to_dict()
    cerere = output["name"]
    count = 0
    for i in cerere:
        if i == ';':
            count = count+1
    subcereri = cerere.split(";",count)
    name=[]
    model=["Create directory at [path]/[directory name]","Create empty file at [path]/[file.ext]","Delete directory from [path]/[directory name]","Delete file from [path]/[file.ext]","Move file [file.ext] to [path]","Rename file [file.ext] to [newfile.ext]","Replace text [your-text] with [new-text] in file [file.ext]","Delete empty lines from [path]/[file.ext]","Print lines matching [pattern] from [path]/[file.ext]"]
    option = request.form['options']
    if (option == "linux"):
        os = 2
    else:
        os = 3
    corect = 0
    for i in subcereri:

        ## Pentru model cu comenzi in baza de date
        ## Pentru fiecare comanda, cererea o sa arate intr-un anumit fel
        ## Ex: Create a directory: Create directory at [path]/[directory name]
        ## In baza de date putem avea o coloana cu comanda in sine si un identificator, spre ex. primele 2 cuvinte din cerere
        ## Codu de mai jos o sa se schimbe intr-un name.append(*interogare baza de date pe baza primelor 2 cuvinte din cerere* + ...)
        ## Poate o sa mai fie un if sau poate mai multe, s-ar putea sa fie niste cazuri speciale
        impartire = i.split(" ")
        if len(impartire) == 4:
            if impartire[2] != "at" and impartire[2] != "from":
                flash("The request was incorrect!", "warning")
                redirect(url_for("home"))
                return render_template("index.html")
        else:
            if len(impartire) == 5:
                if impartire[0] == "Create" and impartire[1] == "empty":
                    if impartire[2] != "file" or impartire[3] != "at":
                        flash("The request was incorrect!", "warning")
                        redirect(url_for("home"))
                        return render_template("index.html")
                if impartire[0] == "Move" and impartire[1] == "file":
                    if impartire[3] != "to":
                        flash("The request was incorrect!", "warning")
                        redirect(url_for("home"))
                        return render_template("index.html")
                if impartire[0] == "Rename" and impartire[1] == "file":
                    if impartire[3] != "to":
                        flash("The request was incorrect!", "warning")
                        redirect(url_for("home"))
                        return render_template("index.html")
                if impartire[0] == "Delete" and impartire[1] == "empty":
                    if impartire[2] != "lines" or impartire[3]!="from":
                        flash("The request was incorrect!", "warning")
                        redirect(url_for("home"))
                        return render_template("index.html")
            else:
                if len(impartire) == 6:
                    if impartire[0] == "Print" and impartire[1] == "lines":
                        if impartire[2] != "matching" or impartire[4] != "from":
                            flash("The request was incorrect!", "warning")
                            redirect(url_for("home"))
                            return render_template("index.html")
                else:
                    if len(impartire) == 8:
                        if impartire[0] == "Replace" and impartire[1] == "text":
                            if impartire[3] != "with" or impartire[5] != "in" or impartire[6]!= "file":
                                flash("The request was incorrect!", "warning")
                                redirect(url_for("home"))
                                return render_template("index.html")
                    else:
                        flash("The request was incorrect!", "warning")
                        redirect(url_for("home"))
                        return render_template("index.html")
        for x in range(2): # 0 1
            if ((i.split(" ")[0] + " " + i.split(" ")[1]) == tables[x][1]):
                name.append(tables[x][os] + " " + (i.split(" at ", 1)[1]))
                corect += 1
        for x in range(2,4): # 2 3
            if ((i.split(" ")[0] + " " + i.split(" ")[1]) == tables[x][1]):
                name.append(tables[x][os] + " " + (i.split(" from ", 1)[1]))
                corect += 1
        for x in range(4, 6): # 4 5
            if ((i.split(" ")[0] + " " + i.split(" ")[1]) == tables[x][1]):
                name.append(tables[x][os] + " " + (i.split(" ", 4)[2]) + " " + (i.split(" ", 4)[4]))
                corect += 1

        if ((i.split(" ")[0] + " " + i.split(" ")[1]) == "Replace text"):
            name.append(tables[6][os] + " " + (i.split(" ", 7)[7]) + ") " + "-replace " + "'" + (
            i.split(" ", 7)[2]) + "'" + ", " + "'" + (i.split(" ", 7)[4]) + "'" + "|" + "Out-File " + (
                        i.split(" ", 7)[7]))
            corect += 1
        if ((i.split(" ")[0] + " " + i.split(" ")[1]) == "Delete empty"):
            name.append(
                tables[7][3] + " " + (i.split(" ", 4)[4]) + ") | ? {$_.trim() -ne ""} | set-content " + (
                i.split(" ", 4)[4]))
            corect += 1
        if ((i.split(" ")[0] + " " + i.split(" ")[1]) == "Print lines"):
            name.append(tables[8][3] + " " + i.split(" ", 5)[3] + " " + i.split(" ", 5)[5])
            corect += 1

    if corect != len(subcereri):
        flash("The request was incorrect!", "warning")
        redirect(url_for("home"))
        return render_template("index.html")
    else:
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
        path = ".\script.txt"
        return send_file(path, as_attachment=True)
    else:
        file=open("script.txt", "w")
        for i in script_download:
            file.write(i + "\n")
        file.close()
        path = ".\script.txt"
        return send_file(path, as_attachment=True)

if __name__=='__main__':
    app.run(debug=True)