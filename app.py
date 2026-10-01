import sqlite3
from flask import Flask, g, jsonify, request, send_from_directory

DB = "jojo.db"
app = Flask(__name__, static_folder="static")


# ---------- Capa de base de datos ----------

def get_db():
    # Una conexión por petición, guardada en `g` (almacén temporal de Flask).
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row  # filas accesibles por nombre: fila["nombre"]
    return g.db


@app.teardown_appcontext
def close_db(exc):
    # Flask llama esto al terminar cada petición: cerramos la conexión.
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DB)
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS personajes (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre    TEXT NOT NULL,
            parte     TEXT NOT NULL,
            stand     TEXT DEFAULT '',
            habilidad TEXT DEFAULT '',
            notas     TEXT DEFAULT ''
        )
        """
    )
    db.commit()
    db.close()


# ---------- Rutas ----------

@app.get("/")
def index():
    return send_from_directory("static", "index.html")


@app.get("/api/personajes")
def listar():
    q = request.args.get("q", "").strip()
    parte = request.args.get("parte", "").strip()

    sql = """SELECT * FROM personajes
             WHERE (nombre LIKE ? OR stand LIKE ? OR habilidad LIKE ? OR notas LIKE ?)"""
    params = [f"%{q}%"] * 4
    if parte:
        sql += " AND parte = ?"
        params.append(parte)
    sql += " ORDER BY id DESC"

    filas = get_db().execute(sql, params).fetchall()
    return jsonify([dict(f) for f in filas])


@app.post("/api/personajes")
def crear():
    d = request.get_json(silent=True) or {}
    nombre = (d.get("nombre") or "").strip()
    parte = (d.get("parte") or "").strip()
    if not nombre or not parte:
        return jsonify(error="nombre y parte son obligatorios"), 400

    db = get_db()
    cur = db.execute(
        "INSERT INTO personajes (nombre, parte, stand, habilidad, notas) VALUES (?, ?, ?, ?, ?)",
        (nombre, parte, d.get("stand", "").strip(), d.get("habilidad", "").strip(), d.get("notas", "").strip()),
    )
    db.commit()
    fila = db.execute("SELECT * FROM personajes WHERE id = ?", (cur.lastrowid,)).fetchone()
    return jsonify(dict(fila)), 201


@app.delete("/api/personajes/<int:pid>")
def borrar(pid):
    db = get_db()
    cur = db.execute("DELETE FROM personajes WHERE id = ?", (pid,))
    db.commit()
    if cur.rowcount == 0:
        return jsonify(error="no existe"), 404
    return "", 204


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
