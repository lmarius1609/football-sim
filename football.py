import sqlite3
from flask import Flask, redirect, url_for, render_template, request
from module_db import *
from module_sim import calculate_matches

app = Flask(__name__)

@app.route("/")
def home():
  con = db_connect()
  cur = con.cursor()
  cur.execute("SELECT * FROM Teams")
  rows = cur.fetchall()
  rows.sort(key=lambda tup: tup[7])
  rows.reverse()

  headings1 = ("ID", "Team", "Win", "Draw", "Loss", "Goals Marked", "Goals Received", "Points")
  headings2 = ("Team 1", "Team 2", "Goals 1", "Goals 2")

  next_round = get_next_round()
  print('costel', next_round[0],'Gigel', next_round[1])

  currents = []
  nexts = []

  if next_round[0] != 'empty':
    cur.execute("SELECT TEAM1, TEAM2, GOALS1, GOALS2 FROM "+next_round[1]+" WHERE ROUND="+str(next_round[0]-1))
    currents = cur.fetchall()
    cur.execute("SELECT TEAM1, TEAM2 FROM "+next_round[1]+" WHERE ROUND="+str(next_round[0]))
    nexts = cur.fetchall()

  teams_status = calculate_teams_status()
  rounds_status = calculate_rounds_status()
  matches_status = calculate_matches_status()

  return render_template("index.html", headings1=headings1, headings2=headings2, data=rows, currents=currents, nexts=nexts, teams_status=teams_status, rounds_status=rounds_status, matches_status=matches_status)

@app.route("/login", methods=["POST", "GET"])
def login():
   if request.method == "POST":
      inp = request.form
      name = inp["nm"]

      con = db_connect()
      cur = con.cursor()
      cur.execute("SELECT * FROM Teams")
      rows = cur.fetchall()
      
      print('Smantana', type(name))
      if len(rows) <= 10:
        cur.execute("INSERT INTO Teams (NAME) VALUES (?)", (name,))
        con.commit()
        return 'Team added! ' + 'There are ' + str(str(len(rows)+1) + ' teams in the DB.')
      else:
        return 'Error: You cannot add more than 10 teams'
   else:
      return render_template("login.html")

@app.route("/teams")
def teams():
  con = db_connect()
  cur = con.cursor()
  cur.execute("SELECT ID, NAME FROM Teams")
  rows = cur.fetchall()

  headings = ("ID", "Name")
  # return f"<h1>{rows}</h1>"
  return render_template("teams.html", headings=headings, data=rows)

@app.route("/matches")
def matches():
  con = db_connect()
  cur = con.cursor()
  cur.execute("SELECT * FROM Tur")
  rows = cur.fetchall()

  headings = ("ID", "Round", "Team 1", "Team 2", "Goals 1", "Goals 2")
  # return f"<h1>{rows}</h1>"
  return render_template("teams.html", headings=headings, data=rows)

@app.route("/ranking")
def ranking():
  con = db_connect()
  cur = con.cursor()
  cur.execute("SELECT * FROM Teams")
  rows = cur.fetchall()
  rows.sort(key=lambda tup: tup[7])
  rows.reverse()

  headings = ("ID", "Team 1", "Town", "Points")
  # return f"<h1>{rows}</h1>"
  return render_template("teams.html", headings=headings, data=rows)

@app.route("/simulate")
def simulate():
  current_round = get_next_round()
  matches_status = calculate_matches_status()
  if current_round[0] != 'empty' and matches_status != 'Matches not yet generated':
    simulate_round(current_round[0], current_round[1])
    db_add_stats(current_round[0], current_round[1])
    return 'Next Round Simulated'
  elif current_round[0] == 'empty' and matches_status == 'Matches not yet generated':
    return 'Cannot simulate, Matches not generated'
  else:
    return 'All rounds allready simulated'

if __name__ == "__main__":
  create_tables()
  my_teams = get_teams()
  print('My teams are:', my_teams)
  next_round = get_next_round()
  print('costel', next_round[0],'Gigel', next_round[1])
  teams_status = calculate_teams_status()
  calculate_matches(my_teams)


# # For this to work, table row ID's should be the initial ones
#   var1 = total_rounds()
#   var2 = total_round_matches()
#   ids = []

#   if var2 != 0:
#     for k in range(1, var1*var2, var2):
#       ids.append(k)

#   print(ids)

#   # Simulate the whole half season
#   for x in range(1, len(ids) + 1):
#     simulate_round(x, ids[x-1])

#   calculate_points()

  app.run()