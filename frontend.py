from flask import Flask, g, render_template_string, send_file
import sqlite3
import io

app = Flask(__name__)
DB = 'screenshots.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB)
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    db = get_db()
    cur = db.execute('SELECT id, timestamp FROM shots ORDER BY id DESC')
    shots = cur.fetchall()
    return render_template_string('''
    <h1>Screenshot Gallery</h1>
    {% for id, ts in shots %}
      <div>
        <p>{{ ts }}</p>
        <img src="/shot/{{ id }}" style="max-width:400px; border:1px solid #ccc; margin-bottom:20px;">
      </div>
    {% else %}
      <p>No screenshots yet.</p>
    {% endfor %}
    ''', shots=shots)

@app.route('/shot/<int:id>')
def shot(id):
    db = get_db()
    cur = db.execute('SELECT img FROM shots WHERE id=?', (id,))
    row = cur.fetchone()
    if row is None:
        return "Not found", 404
    img_data = row[0]
    return send_file(io.BytesIO(img_data), mimetype='image/png')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
