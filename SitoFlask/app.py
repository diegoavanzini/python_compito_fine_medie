from flask import Flask, render_template, request, redirect
from DB_Operations import init_db, add_compiti, get_compiti, delete_compiti, get_school_subjects

app = Flask(__name__)

# Initialize database on startup
init_db()

@app.route('/')
def home():
    compiti = get_compiti()
    school_subjects = get_school_subjects()
    return render_template('index.html' , compiti=compiti, school_subjects=school_subjects)

@app .route("/compiti" , methods=["GET"]) 
def compiti(): 
    return get_compiti()

@app .route("/delete" , methods=["POST"])
def delete():
    if request.method == "POST"  :
        id = request.form["id_compiti"]
        delete_compiti(id)
        return redirect("/") 

@app.route("/compiti", methods=["POST"]) 
def  AddText(): 
    if request.method == "POST" : 
        title = request.form["title"] 
        description = request.form["description"]
        materia = request.form["materia"]
        data_scadenza = request.form["scadenza"]
        #salvataggio di tutti i valori nel db
        add_compiti(title, description, data_scadenza, materia) 
        return redirect("/") 

if __name__ == '__main__':
    app.run(port=5050, debug=True)
