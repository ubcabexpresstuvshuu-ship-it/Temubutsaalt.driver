# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template_string, redirect, url_for, session
import os

app = Flask(_name_)
# Session-д заавал нууц түлхүүр хэрэгтэй (Render дээр ENV-аас уншина)
app.secret_key = os.environ.get("TEMU_SECRET_KEY", "temu_secret_2025")

# -------- Өгөгдөл (жишээ) --------
DUUREGUUD = [
    {"id": 1, "name": "Хан-Уул", "zip": 17},
    {"id": 2, "name": "Баянзүрх", "zip": 13},
    {"id": 3, "name": "Сонгинохайрхан", "zip": 18},
    {"id": 4, "name": "Баянгол", "zip": 15},
    {"id": 5, "name": "Чингэлтэй", "zip": 16},
    {"id": 6, "name": "Налайх", "zip": 22},
    {"id": 7, "name": "Багануур", "zip": 21},
    {"id": 8, "name": "Багахангай", "zip": 20},
]

USERS = {
    "admin":  {"password": "1234", "role": "admin"},
    "driver": {"password": "0000", "role": "driver"},
}

@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("admin_panel" if session["role"]=="admin" else "driver_panel"))
    return redirect(url_for("login"))

# ------------- Login -------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form.get("username","").strip()
        p = request.form.get("password","").strip()
        info = USERS.get(u)
        if info and info["password"] == p:
            session["user"] = u
            session["role"] = info["role"]
            return redirect(url_for("admin_panel" if info["role"]=="admin" else "driver_panel"))
        return "<h3>Нэвтрэх нэр/нууц үг буруу</h3><a href='/login'>Буцах</a>"

    return render_template_string("""
    <h2>Нэвтрэх</h2>
    <form method="post">
      <input name="username" placeholder="Нэвтрэх нэр"><br>
      <input name="password" type="password" placeholder="Нууц үг"><br>
      <button type="submit">Нэвтрэх</button>
    </form>
    """)

# ------------ Admin --------------
@app.route("/admin")
def admin_panel():
    if "user" not in session or session["role"] != "admin":
        return redirect(url_for("login"))
    items = "".join([f"<li>{d['name']} — ZIP {d['zip']}</li>" for d in DUUREGUUD])
    return f"<h2>Админ хэсэг</h2><ul>{items}</ul><a href='/logout'>Гарах</a>"

# ------------ Driver -------------
@app.route("/driver")
def driver_panel():
    if "user" not in session or session["role"] != "driver":
        return redirect(url_for("login"))
    items = "".join([f"<li>{d['name']}</li>" for d in DUUREGUUD])
    return f"<h2>Жолоочийн хэсэг</h2><p>Сайн уу, {session['user']}!</p><ul>{items}</ul><a href='/logout'>Гарах</a>"

# ------------- API ---------------
@app.route("/api/duureg")
def api_duureg():
    return jsonify(DUUREGUUD)

# ----------- Logout --------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ----------- Run (локалд) --------
if _name_ == "_main_":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
