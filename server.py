from flask import Flask, request, jsonify, send_from_directory
import sqlite3, random, string, smtplib
from email.mime.text import MIMEText
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder="public")
DB = "forum.db"

def db():
    return sqlite3.connect(DB)

def gen_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def send_verification(email, code):
    with open("verification-email.html") as f:
        html = f.read().replace("{{CODE}}", code)

    msg = MIMEText(html, "html")
    msg["Subject"] = "Verify your Forum account"
    msg["From"] = "YOUR_EMAIL@gmail.com"
    msg["To"] = email

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("YOUR_EMAIL@gmail.com", "APP_PASSWORD")
    server.send_message(msg)
    server.quit()

@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json
    code = str(random.randint(100000, 999999))

    con = db()
    try:
        con.execute(
            "INSERT INTO users (email, password_hash, verification_code) VALUES (?, ?, ?)",
            (data["email"], generate_password_hash(data["password"]), code)
        )
        con.commit()
    except:
        return jsonify({"error": "Email exists"}), 400

    send_verification(data["email"], code)
    return jsonify({"ok": True})

@app.route("/api/verify", methods=["POST"])
def verify():
    data = request.json
    con = db()
    cur = con.execute(
        "SELECT id FROM users WHERE email=? AND verification_code=?",
        (data["email"], data["code"])
    )
    user = cur.fetchone()
    if not user:
        return jsonify({"error": "Invalid code"}), 400

    con.execute("UPDATE users SET verified=1 WHERE email=?", (data["email"],))
    con.commit()
    return jsonify({"ok": True})

@app.route("/api/community", methods=["POST"])
def create_community():
    data = request.json
    con = db()
    con.execute("INSERT INTO communities (name, creator_id) VALUES (?, ?)",
                (data["name"], data["user_id"]))
    con.commit()
    return jsonify({"ok": True})

@app.route("/api/post", methods=["POST"])
def create_post():
    data = request.json
    pid = gen_id()
    slug = data["title"].lower().replace(" ", "-")

    con = db()
    con.execute(
        "INSERT INTO posts VALUES (?, ?, ?, ?, ?)",
        (pid, data["community"], data["title"], slug, data["user_id"])
    )
    con.commit()

    return jsonify({
        "url": f"/f/{data['community']}/p/{pid}/{slug}"
    })

@app.route("/api/post/<pid>")
def get_post(pid):
    con = db()
    cur = con.execute("SELECT * FROM posts WHERE id=?", (pid,))
    post = cur.fetchone()
    if not post:
        return jsonify({"error": "Not found"}), 404

    return jsonify({
        "id": post[0],
        "community": post[1],
        "title": post[2],
        "slug": post[3]
    })

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    return send_from_directory("public", "index.html")

def init_db():
    con = sqlite3.connect(DB)
    con.executescript("""
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      email TEXT UNIQUE,
      password_hash TEXT,
      verified INTEGER DEFAULT 0,
      verification_code TEXT
    );

    CREATE TABLE IF NOT EXISTS communities (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT UNIQUE,
      creator_id INTEGER
    );

    CREATE TABLE IF NOT EXISTS posts (
      id TEXT PRIMARY KEY,
      community TEXT,
      title TEXT,
      slug TEXT,
      author_id INTEGER
    );
    """)
    con.commit()
    con.close()


app.run(debug=True)
