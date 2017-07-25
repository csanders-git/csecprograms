import csv
import sqlite3
from flask import Flask, g

app = Flask(__name__)

def init_db(db):
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
        db.commit()

def get_db():
    db = sqlite3.connect("data.db")
    cur = db.cursor()
    results = cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    found = False
    for table in results:
        if table[0] == "program_report":
            found = True
    if found is False:
        init_db(db)
    return db

def main():
    db = get_db()
    entries = []
    text = [0,1,2,7,9,11,13,15,17,19,22,24]
    ints = [3,4,5,6,8,10,12,14,16,18,20,21,23,25,26,27,28,29,30,31,32,33,34,35,36,37,38]
    with open('School_Spreadsheet.csv', 'rU') as f:
        reader = csv.reader(f, dialect=csv.excel_tab)
        for row in reader:
            temp2 = []
            row = row[0].split(',')
            for i, cell in enumerate(row):
                if i in ints and row[i] == '':
                    temp2.append(0)
                elif i in text and row[i] == '':
                    temp2.append("None")
                elif cell == "FALSE":
                    temp2.append(0)
                elif cell == "TRUE":
                    temp2.append(1)
                else:
                    temp2.append(cell)
            entries.append(temp2)
    entries = entries[1:]
    print entries[0]
    print len(entries[1])
    print entries
    for record in entries:
        record = [tuple(record)]
        cur = db.cursor()
        try:
            cur.executemany('insert into program_report values \
                ('+('?,'*39)[:-1]+')', record)
            db.commit()
        except sqlite3.ProgrammingError as e:
            pass
            #print record
            #print len(record)
            #print e
main()
