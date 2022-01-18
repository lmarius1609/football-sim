import sqlite3
from random import choices

def db_connect(db_path='marius_db'):
	con = None
	try:
		con = sqlite3.connect(db_path)
		return con
	except Error as e:
		print(e)
	return con

def create_tables():
	con = db_connect()
	cur = con.cursor()

	customers_sql = """
	CREATE TABLE IF NOT EXISTS Teams(
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	NAME TEXT NOT NULL,
    TOWN TEXT,
    POINTS INT)"""
	cur.execute(customers_sql)

	tur_sql = """
	CREATE TABLE IF NOT EXISTS Tur(
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	ROUND INTEGER,
	TEAM1 TEXT,
	TEAM2 TEXT,
	GOALS1 INT,	
    GOALS2 INT)"""
	cur.execute(tur_sql)

	retur_sql = """
	CREATE TABLE IF NOT EXISTS Retur(
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	ROUND INTEGER,
	TEAM1 TEXT,
	TEAM2 TEXT,
	GOALS1 INT,
    GOALS2 INT)"""
	cur.execute(retur_sql)

	con.commit()
	con.close()

def get_teams():
	con = db_connect()
	cur = con.cursor()
	cur.execute("SELECT * FROM Teams")
	rows = cur.fetchall()
	result = []

	for i in range(len(rows)):
		result.append(rows[i][1])
	return tuple(result)

def total_rounds():
	con = db_connect()
	cur = con.cursor()
	cur.execute("SELECT * FROM Teams")
	teams = cur.fetchall()
	return len(teams) -1

def total_round_matches():
	con = db_connect()
	cur = con.cursor()
	cur.execute("SELECT * FROM Teams")
	teams = cur.fetchall()
	return int(len(teams)/2)

def calculate_points():
	con = db_connect()
	cur = con.cursor()
	cur.execute("SELECT * FROM Tur")
	matches = cur.fetchall()
	for match in matches:
		if match[4] > match[5]:
			cur.execute("UPDATE Teams SET POINTS = POINTS + (?) WHERE NAME = (?)", (3, match[2]))
		elif match[4] < match[5]:
			cur.execute("UPDATE Teams SET POINTS = POINTS + (?) WHERE NAME = (?)", (3, match[3]))
		else:
			cur.execute("UPDATE Teams SET POINTS = POINTS + (?) WHERE NAME = (?)", (1, match[2]))
			cur.execute("UPDATE Teams SET POINTS = POINTS + (?) WHERE NAME = (?)", (1, match[3]))
	con.commit()
	con.close()


def simulate_round(rnd, id):
    con = db_connect()
    cur = con.cursor()

    match_goals = 0
    all_goals = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    weights = [0.25, 0.2, 0.17, 0.14, 0.11, 0.06, 0.03, 0.02, 0.01, 0.01]
    round_matches = total_round_matches() + 1
    print(round_matches, 'fff')

    teams = get_teams()
    for i in range(1, round_matches):
    	goals = choices(all_goals, weights)
    	goals = goals[0]
    	cur.execute("UPDATE Tur SET GOALS1 = (?) WHERE ROUND = (?) AND ID = (?)", (goals, rnd, id))
    	goals = choices(all_goals, weights)
    	goals = goals[0]   	
    	cur.execute("UPDATE Tur SET GOALS2 = (?) WHERE ROUND = (?) AND ID = (?)", (goals, rnd, id))
    	id +=1
    con.commit()
    con.close()
