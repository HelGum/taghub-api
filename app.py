from flask import Flask, request, g, jsonify, make_response
from db import DB
from user import User

# Oppgave:  Restful API i python
# API som oppretter brukere i PostgreSQL database

app = Flask(__name__)

@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "POST":
        # opprett bruker
        try:
            id = User.add(request.json["username"], request.json["email"], request.json["password"])
            DB.commit()
            return make_response(jsonify(id=id), 200)
        except:
            DB.rollback()
            return make_response(jsonify(error="User already exists"), 404)
    # returner alle brukerene
    return jsonify([x.__dict__ for x in User.get_all()])

@app.route("/users/<int:id>", methods=["GET", "DELETE"])
def user_by_id(id):
    if request.method == "GET":
        # returnere spesifikk bruker: hvis den ikke eksisterer, returner passende status kode
        try:
            user = User.get(id)
            DB.commit()
            if user:
                return make_response(jsonify(user.__dict__), 200)
        except:
            DB.rollback()
        return make_response(jsonify(error="User doesn't exist"), 404)
    # slett brukeren: hvis den ikke eksisterer, returner passende status kode 
    try:
        deleted_rows = User.delete(id)
        DB.commit()
        if deleted_rows == 1:
            return make_response(jsonify(result="User has been deleted"), 200)
    except:
        DB.rollback()
        return make_response(jsonify(error="User doesn't exist"), 404)


if __name__ == '__main__':
    app.run(debug=True)
