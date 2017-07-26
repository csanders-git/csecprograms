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
        reader = csv.reader(f, dialect=csv.excel)
        next(reader, None)
        for row in reader:
            temp2 = []
            for i, cell in enumerate(row):
                # University
                if i == 0:
                    temp2.append("<a href=\""+str(row[i+1]) + "\">" + str(cell) + "</a>")
                    continue
                if i == 1:
                    continue
                # Research link
                if i == 7:
                    if cell != "FALSE":
                        temp2.append("<a href=\""+cell+"\">True</a>")
                    else:
                        temp2.append("False")
                    continue
                # CS Curr
		if i == 8:
                    if cell != "FALSE":
                        temp2.append("<a href=\""+row[i+1]+"\">True</a>")
                    else:
                        temp2.append("False")
                    continue
                if i == 9:
                    continue
 		# SE
                if i == 10:
                    if cell != "FALSE":
                        temp2.append("<a href=\""+row[i+1]+"\">True</a>")
                    else:
                        temp2.append("False")
                    continue
                if i == 11:
                    continue
 		# IS
                if i == 12:
                    if cell != "FALSE":
                        temp2.append("<a href=\""+row[i+1]+"\">True</a>")
                    else:
                        temp2.append("False")
                    continue
                if i == 13:
                    continue
 		# IT
                if i == 14:
                    if cell != "FALSE":
                        temp2.append("<a href=\""+row[i+1]+"\">True</a>")
                    else:
                        temp2.append("False")
                    continue
                if i == 15:
                    continue
 		# CE
        	if i == 16:
                    if cell != "FALSE":
                        temp2.append("<a href=\""+row[i+1]+"\">True</a>")
                    else:
                        temp2.append("False")
                    continue
                if i == 17:
                    continue

 		# security
                if i == 18:
                    if cell != "FALSE":
                        temp2.append("<a href=\""+row[i+1]+"\">True</a>")
                    else:
                        temp2.append("False")
                    continue
                if i == 19:
                    continue
 
                # minor
                if i == 21:
                    if cell != "FALSE":
                        temp2.append("<a href=\""+row[i+1]+"\">True</a>")
                    else:
                        temp2.append("False")
                    continue
                if i == 22:
                    continue
 
 		# masters
                if i == 23:
                    if cell != "FALSE":
                        temp2.append("<a href=\""+row[i+1]+"\">True</a>")
                    else:
                        temp2.append("False")
                    continue
                if i == 24:
                    continue
 


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
    for record in entries:
        record = [tuple(record)]
        cur = db.cursor()
        try:
            cur.executemany('insert into program_report values \
                ('+('?,'*30)[:-1]+')', record)
            db.commit()
        except sqlite3.ProgrammingError as e:
            print e
            print "\t", str(record)
            pass
main()
