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
  rows.sort(key=lambda tup: tup[3])
  rows.reverse()
  headings = ("ID", "Team 1", "Town", "Points")

  cur.execute("SELECT * FROM Tur WHERE ROUND=1")
  currents = cur.fetchall()
  cur.execute("SELECT * FROM Tur WHERE ROUND=2")
  nexts = cur.fetchall()

  teams_status = calculate_sim_stats()

  rounds_status = ''
  current_round = get_current_round()
  if current_round[0] != 'empty':
    rounds_status = 'Next is Round ' + str(current_round[0]) + ' from ' + str(current_round[1])
  else:
    rounds_status = 'All rounds allready simulated'  

  # return f"<h1>{rows}</h1>"
  return render_template("index.html", headings=headings, data=rows, currents=currents, nexts=nexts, teams_status=teams_status, rounds_status=rounds_status)

@app.route("/login", methods=["POST", "GET"])
def login():
   if request.method == "POST":
      inp = request.form
      name = inp["nm"]
      town = inp["twn"]

      con = db_connect()
      cur = con.cursor()
      cur.execute("SELECT * FROM Teams")
      rows = cur.fetchall()
      
      if len(rows) <= 16:
        cur.execute("INSERT INTO Teams (NAME, TOWN) VALUES (?,?)", (name, town))
        con.commit()
        return 'Team added! ' + 'There are ' + str(str(len(rows)+1) + ' teams in the DB.')
      else:
        return 'Error: You cannot add more than 16 teams'
   else:
      return render_template("login.html")

@app.route("/teams")
def teams():
  con = db_connect()
  cur = con.cursor()
  cur.execute("SELECT * FROM Teams")
  rows = cur.fetchall()

  headings = ("ID", "Name", "Town")
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
  rows.sort(key=lambda tup: tup[3])
  rows.reverse()

  headings = ("ID", "Team 1", "Town", "Points")
  # return f"<h1>{rows}</h1>"
  return render_template("teams.html", headings=headings, data=rows)

@app.route("/simulate")
def simulate():
  current_round = get_current_round()
  if current_round[0] != 'empty':
    simulate_round(current_round[0], current_round[1])
    return 'Next Round Simulated'
  else:
    return 'All rounds allready simulated'

if __name__ == "__main__":
  create_tables()
  my_teams = get_teams()
  print('My teams are:', my_teams)
  teams_status = calculate_sim_stats()
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