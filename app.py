import sqlite3
import os
import time
import shutil
import zipfile
import gzip
import tldextract
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, g

app = Flask(__name__)

app.config["DATABASE"] = "data.db"

def init_db(db):
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
        db.commit()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        cur = db.cursor()
        results = cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        found = False
        for table in results:
            if table[0] == "program_report":
                found = True
        if found is False:
            init_db(db)
    return db

@app.route('/')
def index():
    get_db()
    key = request.args.get('operation')
    message = ''
    if key == "True":
        message = "Added DMARC data succesfully"
    return render_template('index.html', message=message)

@app.route('/data',methods=['GET','POST'])
def data():
    epochs = -1
    epoche = -1
    db = get_db()
    cursor = db.execute("SELECT * from program_report")
    tablecontent = ''
    for row in cursor:
        onerow = '<tr>\n'
        for ind, element in enumerate(row):
            if element == 1:
                 onerow += "\t<td>True</td>\n"
            elif element == 0:
                 onerow += "\t<td>False</td>\n"
            else:
                onerow += "\t<td>"+str(element)+"</td>\n"
        onerow += '</tr>\n'
        tablecontent += onerow
    return render_template('data.html', tc=tablecontent)

def dict_factory(cursor, row):
    d_out = {}
    for idx, col in enumerate(cursor.description):
        d_out[col[0]] = row[idx]
    return d_out

@app.route('/stats')
def stats():
    db = get_db()
    tablecontent = ''
    db.row_factory = dict_factory
    cursor = db.execute("SELECT spf_domain from program_report")
    tablecontent = ''
    domains = {}
    for row in cursor:
        extracted = tldextract.extract(row["spf_domain"])
        domain = "{}.{}".format(extracted.domain, extracted.suffix)
        try:
            domains[domain] += 1
        except KeyError:
            domains[domain] = 1
    for domain, count in domains.iteritems():
        tablecontent += "<tr>\n"
        tablecontent += "\t<td>"+str(domain)+"</td>\n"
        tablecontent += "\t<td>"+str(count)+"</td>\n"
        tablecontent += "</tr>\n"
    return render_template('stats.html', tc=tablecontent)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("8080"),
        debug=True
    )
