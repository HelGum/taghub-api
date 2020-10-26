import psycopg2

DATABASE_DB = "taghub_task"
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "xxx"

class DB:

    conn = None

    @classmethod
    def cursor(cls):
        if not cls.conn:
            cls.conn = psycopg2.connect(dbname=DATABASE_DB, user=DATABASE_USER, 
            password=DATABASE_PASSWORD)
        return cls.conn.cursor()

    @classmethod
    def commit(cls):
        cls.conn.commit()

    @classmethod
    def rollback(cls):
        cls.conn.rollback()
    
    @classmethod
    def close(cls):
        cls.conn.close()
        cls.conn = None