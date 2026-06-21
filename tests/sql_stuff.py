#relearning some of the SQL stuff and making sure it works before I work on it with the actual game 
import sqlite3 as sql

amounclicks = 0

def updatesave(amountclicks):
    connection = sql.connect("test.db", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(f'UPDATE save_files SET amount_clicks = ? WHERE rowid = 1', (amountclicks,))
    connection.commit()
    connection.close()

def loadsave():
    global amounclicks
    connection = sql.connect("test.db", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM save_files")
    details = cursor.fetchone()
    print(details)
    for var in details:
        amounclicks = var

updatesave(6)
loadsave()
print(f"{amounclicks} = amount of clicks")