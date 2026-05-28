import sqlite3
import datetime

def init_db():
    """Initialize database tables at startup"""
    connection = sqlite3.connect("compiti.db")
    cursor = connection.cursor()
    
    # Create compiti table
    cursor.execute("""CREATE TABLE IF NOT EXISTS "compiti" (
	"id"	INTEGER,
	"descrizione"	TEXT,
	"titolo"	TEXT,
    "materia"    TEXT,
	"data_scadenza"	DATETIME,
	"creation_date"	DATETIME,
	"update_date"	DATETIME default current_timestamp,
	PRIMARY KEY("id" AUTOINCREMENT)
);""")
    
      
    # Create school_subjects table
    cursor.execute("""CREATE TABLE IF NOT EXISTS "school_subjects" (
    "id"	INTEGER,
    "subject"	TEXT,
    "creation_date"	DATETIME,
    "update_date"	DATETIME default current_timestamp,
    PRIMARY KEY("id" AUTOINCREMENT)
);""")
    
    # Insert default school subjects if table is empty
    cursor.execute("SELECT COUNT(*) FROM school_subjects")
    if cursor.fetchone()[0] == 0:
        default_subjects = [
            "Matematica",
            "Italiano",
            "Inglese",
            "Storia",
            "Geografia",
            "Scienze",
            "Educazione Fisica",
            "Spagnolo",
            "Arte",
            "Musica",
            "Religione",
            "Tecnologia",
            "Strumento"
        ]
        for subject in default_subjects:
            cursor.execute(
                "INSERT INTO school_subjects (subject, creation_date) VALUES (?, ?)",
                (subject, datetime.datetime.now())
            )
    
     # Create subjects_days table
    cursor.execute("""CREATE TABLE IF NOT EXISTS "subjects_days" (
    "id"	INTEGER,
    "id_subject"	INTEGER,
    "id_week_day"	INTEGER,
    "creation_date"	DATETIME,
    "update_date"	DATETIME default current_timestamp,
    PRIMARY KEY("id" AUTOINCREMENT)
);""")
    # Insert default school subjects schedule if table is empty
    cursor.execute("SELECT COUNT(*) FROM subjects_days")
    if cursor.fetchone()[0] == 0:
        # List of (week_day_id, subject_id) tuples
        # week_day_id: 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday, 6=Saturday, 7=Sunday
        # subject_id: corresponds to ID in school_subjects table
        subjects_days = [
            (1, 9), (1, 1), (1, 8), (1, 2), (1, 4),
            (2, 12), (2, 3), (2, 2), (2, 1),
            (3, 1), (3, 6), (3, 8), (3, 10), (3, 11), (3, 2),
            (4, 7), (4, 3), (4, 2), (4, 6), (4, 4),
            (5, 10),(5, 9), (5, 5), (5, 1), (5, 3)
        ]
        for week_day_id, subject_id in subjects_days:
            cursor.execute(
                "INSERT INTO subjects_days (id_week_day, id_subject, creation_date) VALUES (?, ?, ?)",
                (week_day_id, subject_id, datetime.datetime.now())
            )
    connection.commit()
    connection.close()

def get_compiti():
    connection = sqlite3.connect("compiti.db")
    cursor = connection.cursor()
    cursor.row_factory = sqlite3.Row
    cursor.execute("""SELECT id, descrizione, titolo, data_scadenza FROM COMPITI;""")
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]

def get_school_subjects():
    connection = sqlite3.connect("compiti.db")
    cursor = connection.cursor()
    cursor.row_factory = sqlite3.Row
    cursor.execute("""SELECT DISTINCT id, subject FROM school_subjects;""")
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]

#inserting data to db
def add_compiti(title, description, data_scadenza, materia):
    connection = sqlite3.connect("compiti.db")
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO compiti(titolo, descrizione, data_scadenza, materia, creation_date) 
                   VALUES (?,?,?,?,?)"""
                   , (title, description, data_scadenza, materia, datetime.datetime.now()))
    connection.commit()
    connection.close()
    return 1

def delete_compiti(id):
    connection = sqlite3.connect("compiti.db")
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM compiti WHERE id = ? """, (id,))
    connection.commit()
    connection.close()
    return 1

def get_data_scadenza(materia):
    result = []
    connection = sqlite3.connect("compiti.db")
    cursor = connection.cursor()
    cursor.row_factory = sqlite3.Row
    # Data corrente e numero del giorno della settimana (lunedi=1 ... domenica=7)
    oggi = datetime.datetime.now() 
    numero_giorno_oggi = oggi.weekday() + 1 
    # Recupera tutti i giorni in cui e prevista la materia, ordinati cronologicamente
    cursor.execute("""SELECT id_week_day 
                   FROM subjects_days as sd 
                   INNER JOIN school_subjects as ss 
                   ON ss.id = sd.id_subject 
                   WHERE subject = ? ORDER by id_week_day ASC""", (materia,))
    rows = cursor.fetchall()
    connection.close()
    if not rows:  # or just "if row"
        return result

    # Converte le righe del DB in una lista semplice di interi (giorni settimana)
    week_days = []
    for r in rows:
         week_days.append(r[0])

    # Cerca le prossime 2 date utili per la materia
    for d in week_days:
        if len(result) >= 2:
            break
        if d > numero_giorno_oggi + 2:
            # Giorno sufficientemente nel futuro: calcola direttamente la prossima data
            next_day = d
            delta_giorni = next_day - numero_giorno_oggi
            result.append(oggi + datetime.timedelta(days = delta_giorni))
        else:
            # Giorno gia passato o troppo vicino: lo sposta alla settimana successiva
            giorno_posticipato = d + 7
            week_days.append(giorno_posticipato)
    
    return result