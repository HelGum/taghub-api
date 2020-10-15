from flask import Flask, request, g, jsonify, render_template
import psycopg2

# Oppgave:  Restful API i python
# API som oppretter brukere i PostgreSQL database

app = Flask(__name__)

app.config["DATABASE_USER"] = "postgres"
app.config["DATABASE_PASSWORD"] = "xxx"
app.config["DATABASE_DB"] = "taghub_task"

def get_db():
    if not hasattr(g, "_database"):
        g._database = psycopg2.connect(dbname=app.config["DATABASE_DB"], user=app.config["DATABASE_USER"], 
            password=app.config["DATABASE_PASSWORD"])
    return g._database

@app.teardown_appcontext
def teardown_db(error):
    """Lukker databasen etter forespørselen er ferdig"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def get_all_users():
    users = []
    conn = get_db()
    cur = conn.cursor()
    try:
        sql = "SELECT id, username, email, password FROM users"
        cur.execute(sql)
        for (id, username, email, password) in cur:
            users.append({
                "id": id,
                "username": username,
                "email": email,
                "pasword": password
            })
    finally:
        cur.close()
    return users

def add_user(username, email, password):
    """returnerer id til brukeren som har blitt lagt til ved suksess og -1 hvis brukeren ikke blir lagt til"""
    conn = get_db()
    cur = conn.cursor()
    try:
        sql = "INSERT INTO users(username, email, password) VALUES (%s, %s, %s) RETURNING id"
        cur.execute(sql, (username, email, password))
        id = cur.fetchone()[0]
        conn.commit()
    except psycopg2.Error as e:
        id = -1
    finally:
        cur.close()
    return id

def get_user(id):
    """returnerer bruker infromasjon ved suksess og -1 hvis brukeren ikke eksisterer"""
    conn = get_db()
    cur = conn.cursor()
    try:
        sql = "SELECT username, email, password FROM users WHERE id=(%s)"
        cur.execute(sql, (id,))
        user = cur.fetchone()
        if not user:
            user = -1
        else:
            user = {
                "id": id,
                "username": user[0],
                "email": user[1],
                "password": user[2]
            }
    finally:
        cur.close()
    return user

def delete_user(id):
    """returnerer anntall endringer; hvis 0 returneres eksisterer ikke brukeren"""
    conn = get_db()
    cur = conn.cursor()
    try:
        sql = "WITH deleted AS (DELETE FROM users WHERE id = (%s) IS TRUE RETURNING *) SELECT count(*) FROM deleted;"
        cur.execute(sql, (id,))
        deleted_rows = cur.fetchone()[0]
        conn.commit()
    finally:
        cur.close()
    return deleted_rows

@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "POST":
        # opprett bruker
        id = add_user(request.form["username"], request.form["email"], request.form["password"])
        if id != -1:
            return make_response(jsonify(id=id), 200)
        else:
            return make_response(jsonify(error="User already exists"), 404)
    # list opp alle brukerene
    user_list = get_all_users()
    return jsonify(user_list)

@app.route("/users/<int:id>", methods=["GET", "DELETE"])
def user_by_id(id):
    if request.method == "GET":
        # returnere spesifikk bruker: hvis den ikke eksisterer, returner passende status kode
        user = get_user(id)
        if user != -1:
            return make_response(jsonify(user), 200)
        else:
            return make_response(jsonify(error="User doesn't exist"), 404)
    # slett brukeren: hvis den ikke eksisterer, returner passende status kode 
    if delete_user(id) != 0:
        return make_response(jsonify(result="User has been deleted"), 200)
    else:
        return make_response(jsonify(error="User doesn't exist"), 404)

if __name__ == '__main__':
    app.run(debug=True)
