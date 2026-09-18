import mysql.connector as SQLC

def connect():
    DataBase = SQLC.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "ff_db"
    )
    return DataBase