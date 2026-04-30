from src.scadenza import calcolo_scadenza
from src.repository import scrivi
import gettext
import argparse
import os

parser = argparse.ArgumentParser(description="Descrizione del tuo script")

parser.add_argument("-l", "--language", type=str, help="La tua lingua")

args = parser.parse_args()

localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')

translate = gettext.translation('main', localedir, languages=[args.language], fallback=True)
translate.install()

def inserisci_compito(input_data_compito,input_nome_compito,input_descrizione_compito):
    data_avviso = calcolo_scadenza(input_data_compito)
    dati_compito = input_nome_compito + ";" + input_descrizione_compito+";"+ input_data_compito + ";" +  data_avviso + "\n"
    scrivi("compiti.txt", dati_compito)
    return data_avviso

parser = argparse.ArgumentParser(description="Descrizione del tuo script")

parser.add_argument("-l", "--language", type=str, help="La tua lingua")

args = parser.parse_args()

s = True
n = False

proposta = input(_("Do you want to add a task to the list? (y/n)"))       
y = _("y")

if proposta == y:
    input_nome_compito = input(_("enter the name of the task:"))
    input_descrizione_compito = input(_("enter the task description:"))
    input_data_compito = input(_("Enter the expiration date: (dd/mm/yyyy)"))
    data_avviso = inserisci_compito(input_data_compito,input_nome_compito,input_descrizione_compito)
    print(_("ok, I will notify you the day"),data_avviso,_("that is, one day before the assignment"))

print(_("passiamo agli avvisi di oggi"))

memory_file = open("compiti.txt", "r", encoding = "utf8")
contenuto_file = memory_file.read()
print(contenuto_file)
memory_file.close()


