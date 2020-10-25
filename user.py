from db import DB

class User:

    def __init__(self, id, username, email, password):
        self.id = id
        self.name = username
        self.email = email
        self.pwd= password

    @classmethod
    def get(cls, id):
        """returnerer bruker infromasjon ved suksess og None hvis brukeren ikke eksisterer"""
        cur = DB.cursor()
        try:
            sql = "SELECT username, email, password FROM users WHERE id=(%s)"
            cur.execute(sql, (id,))
            row = cur.fetchone()
            if row:
                return cls(id, *row)
        finally:
            cur.close()
        return None
    
    @classmethod
    def get_all(cls):
        users = []
        cur = DB.cursor()
        try:
            sql = "SELECT id, username, email, password FROM users"
            cur.execute(sql)
            for (id, username, email, password) in cur:
                users.append(cls(id, username, email, password))
        finally:
            cur.close()
        return users
    
    @staticmethod
    def delete(id):
        """returnerer anntall endringer; hvis 0 returneres eksisterer ikke brukeren"""
        cur = DB.cursor()
        try:
            sql = "WITH deleted AS (DELETE FROM users WHERE id = (%s) IS TRUE RETURNING *) SELECT count(*) FROM deleted;"
            cur.execute(sql, (id,))
            deleted_rows = cur.fetchone()[0]
        finally:
            cur.close()
        return deleted_rows

    @staticmethod
    def add(username, email, password):
        """returnerer id til brukeren som har blitt lagt til ved suksess og -1 hvis brukeren ikke blir lagt til"""
        cur = DB.cursor()
        try:
            sql = "INSERT INTO users(username, email, password) VALUES (%s, %s, %s) RETURNING id"
            cur.execute(sql, (username, email, password))
            return cur.fetchone()[0]
        finally:
            cur.close

 