import sqlite3
from random import choices

class Team:
    def __init__(self, name='', win=0, draw=0, loss=0, goals_marked=0, goals_received=0, points=0):
        self.name = name
        self.win = win
        self.draw = draw
        self.loss = loss
        self.goals_marked = goals_marked
        self.goals_received = goals_received
        self.points = points

    def calculate_stats(self, goals_mar, goals_rec):
        self.goals_marked = goals_mar
        self.goals_received = goals_rec
        if goals_mar > goals_rec:
            self.win = 1
            self.points = 3
        elif goals_mar == goals_rec:
            self.draw = 1
            self.points = 1
        else:
            self.loss = 1
        result = {'win': self.win, 'draw': self.draw, 'loss': self.loss, 'goals_marked': self.goals_marked, 'goals_received': self.goals_received, 'points': self.points}
        return result

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
    WIN INT,
	DRAW INT,
	LOSS INT,
	GOALS_MARKED INT,
	GOALS_RECEIVED INT,
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

def calculate_teams_status():
	con = db_connect()
	cur = con.cursor()
	cur.execute("SELECT * FROM Teams")
	nr_teams = len(cur.fetchall())
	teams_status = ''
	if nr_teams < 10:
		teams_status = 'There are only ' + str(nr_teams) +  ' teams in DB, need more'
	elif nr_teams == 10:
		teams_status = 'There are 10 Teams in DB, all OK'

	con.close()
	return teams_status

def calculate_rounds_status():
	rounds_status = ''
	current_round = get_next_round()
	if current_round[0] != 'empty':
		rounds_status = 'Next is Round ' + str(current_round[0]) + ' from ' + str(current_round[1])
	else:
		rounds_status = 'All rounds allready simulated'  
	return rounds_status

def calculate_matches_status():
	con = db_connect()
	cur = con.cursor()
	cur.execute("SELECT * FROM Tur")
	rows = cur.fetchall()
	matches_status = ''
	if len(rows) == 0:
		matches_status = 'Matches not yet generated'
	elif len(rows) != 0:
		matches_status = 'All matches generated, tables populated'
	return matches_status
	con.close()

def simulate_round(rnd, which_half):
	all_goals = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
	weights = [0.25, 0.2, 0.17, 0.14, 0.11, 0.06, 0.03, 0.02, 0.01, 0.01]
	
	con = db_connect()
	cur = con.cursor()
	cur.execute("SELECT ID FROM "+which_half+" WHERE ROUND = "+str(rnd))
	my_table = cur.fetchall()
	for element in my_table:
		goals = choices(all_goals, weights)
		goals = goals[0]
		cur.execute("UPDATE "+which_half+" SET GOALS1 = (?) WHERE ROUND = (?) AND ID = (?)", (goals, rnd, element[0]))
		goals = choices(all_goals, weights)
		goals = goals[0]
		cur.execute("UPDATE "+which_half+" SET GOALS2 = (?) WHERE ROUND = (?) AND ID = (?)", (goals, rnd, element[0]))
	con.commit()
	con.close()
	# team1 = Team()
	# new = team1.calculate_stats(3,0)
	# print(new)

def db_add_stats(rnd, which_half):
	my_team = Team()
	con = db_connect()
	cur = con.cursor()
	cur.execute("SELECT TEAM1, TEAM2, GOALS1, GOALS2 FROM "+which_half+" WHERE ROUND = "+str(rnd))
	round_table = cur.fetchall()
	for element in round_table:
		del my_team
		my_team = Team()
		stats_1 = my_team.calculate_stats(element[2], element[3])
		cur.execute("UPDATE TEAMS SET WIN = WIN + (?) WHERE NAME = (?)", (stats_1['win'], element[0]))
		cur.execute("UPDATE TEAMS SET DRAW = DRAW + (?) WHERE NAME = (?)", (stats_1['draw'], element[0]))
		cur.execute("UPDATE TEAMS SET LOSS = LOSS + (?) WHERE NAME = (?)", (stats_1['loss'], element[0]))
		cur.execute("UPDATE TEAMS SET GOALS_MARKED = GOALS_MARKED + (?) WHERE NAME = (?)", (stats_1['goals_marked'], element[0]))
		cur.execute("UPDATE TEAMS SET GOALS_RECEIVED = GOALS_RECEIVED + (?) WHERE NAME = (?)", (stats_1['goals_received'], element[0]))
		cur.execute("UPDATE TEAMS SET POINTS = POINTS + (?) WHERE NAME = (?)", (stats_1['points'], element[0]))
		con.commit()

		del my_team
		my_team = Team()
		stats_2 = my_team.calculate_stats(element[3], element[2])
		cur.execute("UPDATE TEAMS SET WIN = WIN + (?) WHERE NAME = (?)", (stats_2['win'], element[1]))
		cur.execute("UPDATE TEAMS SET DRAW = DRAW + (?) WHERE NAME = (?)", (stats_2['draw'], element[1]))
		cur.execute("UPDATE TEAMS SET LOSS = LOSS + (?) WHERE NAME = (?)", (stats_2['loss'], element[1]))
		cur.execute("UPDATE TEAMS SET GOALS_MARKED = GOALS_MARKED + (?) WHERE NAME = (?)", (stats_2['goals_marked'], element[1]))
		cur.execute("UPDATE TEAMS SET GOALS_RECEIVED = GOALS_RECEIVED + (?) WHERE NAME = (?)", (stats_2['goals_received'], element[1]))
		cur.execute("UPDATE TEAMS SET POINTS = POINTS + (?) WHERE NAME = (?)", (stats_2['points'], element[1]))
		con.commit()

		print('Sandel', element)
		print('Sandel', stats_1)
		print('Sandel', stats_2)	

def get_next_round():
	con = db_connect()
	cur = con.cursor()
	round_result = [None, None]

	cur.execute("SELECT round FROM Tur WHERE GOALS1 IS NULL AND GOALS2 IS NULL LIMIT 1")
	current_round = cur.fetchone()
	print('Costel', current_round)
	if current_round == None:
		print('Tur simulat complet, verificare tabel Retur')
		cur.execute("SELECT round FROM Retur WHERE GOALS1 IS NULL AND GOALS2 IS NULL LIMIT 1")
		current_round = cur.fetchone()
		round_result[1] = 'Retur'
		if current_round != None:
			round_result[0] = current_round[0]

		if current_round == None:
			print('Tur si Retur simulat complet')
			round_result[0] = 'empty'
			round_result[1] = 'empty'
	else:
		print('Meci din tabel Tur')
		round_result[0] = current_round[0]
		round_result[1] = 'Tur'


	print(round_result[0], round_result[1])
	return round_result