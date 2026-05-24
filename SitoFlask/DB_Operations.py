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
            "Arte",
            "Musica",
            "Informatica"
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
            (1, 1),   # Monday: Matematica
            (1, 2),   # Monday: Italiano
            (2, 3),   # Tuesday: Inglese
            (2, 4),   # Tuesday: Storia
            (3, 5),   # Wednesday: Geografia
            (3, 6),   # Wednesday: Scienze
            (4, 7),   # Thursday: Educazione Fisica
            (4, 8),   # Thursday: Arte
            (5, 9),   # Friday: Musica
            (5, 10),  # Friday: Informatica
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
