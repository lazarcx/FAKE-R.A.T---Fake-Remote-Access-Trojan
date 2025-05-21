import socket
import sqlite3
import threading
from datetime import datetime

DB = 'screenshots.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS shots
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  img BLOB)''')
    conn.commit()
    conn.close()

def handle_client(conn, addr):
    print(f"[*] Connected: {addr}")
    # Prvo primimo 8 bajtova koji govore duzinu slike
    length_bytes = conn.recv(8)
    length = int.from_bytes(length_bytes, 'big')
    data = b''
    while len(data) < length:
        packet = conn.recv(4096)
        if not packet:
            break
        data += packet
    print(f"[*] Primljeno {len(data)} bajtova")

    # Sacuvaj u bazu
    conn_db = sqlite3.connect(DB)
    c = conn_db.cursor()
    c.execute("INSERT INTO shots (timestamp, img) VALUES (?, ?)",
              (datetime.now().isoformat(), data))
    conn_db.commit()
    conn_db.close()

    conn.close()

def server(host='0.0.0.0', port=9999):
    init_db()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)
    print(f"[*] Listening on {host}:{port}")

    while True:
        conn, addr = sock.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    server()
