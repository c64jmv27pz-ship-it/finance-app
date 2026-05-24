from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB = "database.db"


# =====================
# DB初期化
# =====================
def init_db():
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS asset(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            current_asset INTEGER,
            income INTEGER,
            expense INTEGER,
            invest INTEGER,
            rate REAL,
            years INTEGER
        )
        """)
        conn.commit()

init_db()


# =====================
# 画面
# =====================
@app.route("/")
def index():
    return render_template("index.html")


# =====================
# 保存API
# =====================
@app.route("/save", methods=["POST"])
def save():
    data = request.json

    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO asset(
            current_asset, income, expense, invest, rate, years
        )
        VALUES (?,?,?,?,?,?)
        """, (
            int(data.get("current_asset", 0)),
            int(data.get("income", 0)),
            int(data.get("expense", 0)),
            int(data.get("invest", 0)),
            float(data.get("rate", 0)),
            int(data.get("years", 0))
        ))
        conn.commit()

    return jsonify({"ok": True})


# =====================
# 履歴API
# =====================
@app.route("/history")
def history():
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("""
        SELECT current_asset, income, expense, invest, rate, years
        FROM asset
        ORDER BY id DESC
        LIMIT 10
        """)
        rows = cur.fetchall()

    return jsonify(rows)


# =====================
# Render対応起動
# =====================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)