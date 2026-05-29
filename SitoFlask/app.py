import gettext
import os

from flask import Flask, render_template, request, redirect, url_for
from DB_Operations import init_db, add_compiti, get_compiti, delete_compiti, get_school_subjects, get_data_scadenza

app = Flask(__name__)

SUPPORTED_LANGUAGES = {"it", "en", "es"}
LOCALE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "locale")


def get_selected_language():
    language = request.args.get("lang") or request.form.get("lang") or "it"
    if language not in SUPPORTED_LANGUAGES:
        return "it"
    return language


def get_translator(language):
    translation = gettext.translation("main", localedir=LOCALE_DIR, languages=[language], fallback=True)
    return translation.gettext

# Initialize database on startup
init_db()

@app.route('/')
def home():
    current_lang = get_selected_language()
    _ = get_translator(current_lang)
    compiti = get_compiti()
    school_subjects = get_school_subjects()
    return render_template('index.html', compiti=compiti, school_subjects=school_subjects, _=_, current_lang=current_lang)

@app .route("/compiti" , methods=["GET"]) 
def compiti(): 
    return get_compiti()


@app .route("/scadenze" , methods=["GET"]) 
def scadenze():
    id_materia = request.args.get("id_materia")
    return get_data_scadenza(id_materia)

@app .route("/delete" , methods=["POST"])
def delete():
    if request.method == "POST"  :
        id = request.form["id_compiti"]
        delete_compiti(id)
        return redirect(url_for("home", lang=get_selected_language())) 

@app.route("/compiti", methods=["POST"]) 
def  AddCompito(): 
    if request.method == "POST" : 
        title = request.form["title"] 
        description = request.form["description"]
        id_materia = request.form["materia"]
        data_scadenza = request.form["scadenza"]
        #salvataggio di tutti i valori nel db
        add_compiti(title, description, data_scadenza, id_materia) 
        return redirect(url_for("home", lang=get_selected_language()))

if __name__ == '__main__':
    app.run(debug=True)