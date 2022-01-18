import sqlite3
from module_db import *

def calculate_matches(*args):
    print(type(args))
    print(args[0])
    if len(args[0]) % 2 != 0:
        return print('Invalid number of teams')
        
    teams = list(args[0])
    n = len(teams)
    matchs = []
    fixtures = []
    tur = []
    retur = []

    return_matchs = []
    for fixture in range(1, n):
        for i in range(int(n/2)):
            matchs.append((teams[i], teams[n - 1 - i]))
            return_matchs.append((teams[n - 1 - i], teams[i]))
        teams.insert(1, teams.pop())
        fixtures.insert(int(len(fixtures)/2), matchs)
        fixtures.append(return_matchs)
        matchs = []
        return_matchs = []

    # for fixture in fixtures:
    #     print(fixture)

    j = int(len(fixtures)/2 +1)
    k = 1

    for i in range(0, int(len(fixtures)/2), 2):
        tur.append(fixtures[i])
        if j <= len(fixtures) - 1:
            tur.append(fixtures[j])
            j += 2

    for i in range(int(len(fixtures)/2), len(fixtures), 2):
        retur.append(fixtures[i])
        if k <= len(fixtures) / 2 - 1:
            retur.append(fixtures[k])
            k += 2

    con = db_connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM Tur")
    rows = cur.fetchall()
    print(len(rows))
    if len(rows) != 0:
        return print('Match table is already populated')
  
    for j in range(len(tur)):
        for k in tur[j]:
            cur.execute("INSERT INTO Tur (ROUND, TEAM1, TEAM2) VALUES (?,?,?)", (j + 1, k[0], k[1]))

    print()
    for j in range(len(retur)):
        for k in retur[j]:
            cur.execute("INSERT INTO Retur (ROUND, TEAM1, TEAM2) VALUES (?,?,?)", (j + 1, k[0], k[1]))
    con.commit()