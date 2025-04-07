from flask import Flask, render_template
import sqlite3
import os

# Set the template directory to be one level up from the app.py file
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
app = Flask(__name__, template_folder=template_dir)

DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')

def get_messages():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT message FROM messages")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

@app.route("/")
def home():
    messages = get_messages()
    return render_template("index.html", messages=messages)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)