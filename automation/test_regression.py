import pytest
import sys
import logging
import names
sys.path.insert(0, '/home/marius/work-okr/football-sim/')
from module_db import *
from module_sim import calculate_matches

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
STDOUT = logging.StreamHandler(stream=sys.stdout)
LOGGER.addHandler(STDOUT)

def empty_db():
	con = db_connect()
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS Teams")
	cur.execute("DROP TABLE IF EXISTS Tur")
	cur.execute("DROP TABLE IF EXISTS Retur")
	con.commit()
	con.close()

def test_max_teams():
    empty_db()
    create_tables()
    for i in range(15):
        add_team(names.get_full_name())
    con = db_connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM Teams")
    rows = cur.fetchall()
    total_teams = len(rows)
    error_msg = add_team('Excelsior Rotterdam')
    LOGGER.info('Checking if the error message for exceeding max teams is present...')
    assert error_msg == 'Error: You cannot add more than 10 teams'
    LOGGER.info('Checking if the number of teams is exactly 10...')
    assert total_teams == 10

def test_calculate_matches():
    empty_db()
    create_tables()
    for i in range(15):
        add_team(names.get_full_name())
    my_teams = get_teams()
    calculate_matches(my_teams)
	
    con = db_connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM Tur")
    rows_tur = cur.fetchall()
    cur.execute("SELECT * FROM Retur")
    rows_retur = cur.fetchall()

    LOGGER.info('Checking individual team position in Tur vs. Retur...')    
    for i in range(len(rows_tur)):
        # print(rows_tur[i][2], rows_retur[i][3])
        assert rows_tur[i][2] == rows_retur[i][3]

    LOGGER.info('Checking if the length of the Tur / Retur table is correct...')
    assert len(rows_tur) == len(rows_retur) == 45

def test_get_next_round():
    empty_db()
    create_tables()
    for i in range(15):
        add_team(names.get_full_name())
    my_teams = get_teams()
    calculate_matches(my_teams)

    con = db_connect()
    cur = con.cursor()

    for i in range(6):
        cur.execute("UPDATE Tur SET GOALS1 = 3 WHERE ROUND = (?)", ([i]))
        cur.execute("UPDATE Tur SET GOALS2 = 3 WHERE ROUND = (?)", ([i]))
    con.commit()
    con.close()

    current_round = get_next_round()
    print(current_round)

    LOGGER.info('Checking if next round is the expected one...')
    assert current_round[0] == 6 and current_round[1] == 'Tur'


def test_calculate_stats():
    LOGGER.info('Checking if stats calculations are correct...')
    empty_db()
    create_tables()
    for i in range(15):
        add_team(names.get_full_name())
    my_teams = get_teams()
    calculate_matches(my_teams)

    team1 = [3, 1, 0, 13, 6, 10]
    team2 = [3, 1, 0, 13, 6, 10]
    team3 = [2, 1, 1, 11, 8, 7]
    team4 = [1, 1, 2, 9, 10, 4]
    team5 = [1, 1, 2, 9, 10, 4]
    team6 = [0, 1, 3, 6, 13, 1]
    team7 = [0, 1, 3, 6, 13, 1]
    team8 = [1, 1, 2, 8, 11, 4]
    team9 = [2, 1, 1, 10, 9, 7]
    team10 = [2, 1, 1, 10, 9, 7]

    con = db_connect()
    cur = con.cursor()
    cur.execute("UPDATE Tur SET GOALS1 = 3 WHERE ROUND = 1")
    cur.execute("UPDATE Tur SET GOALS2 = 0 WHERE ROUND = 1")

    cur.execute("UPDATE Tur SET GOALS1 = 4 WHERE ROUND = 2")
    cur.execute("UPDATE Tur SET GOALS2 = 4 WHERE ROUND = 2")

    cur.execute("UPDATE Tur SET GOALS1 = 4 WHERE ROUND = 3")
    cur.execute("UPDATE Tur SET GOALS2 = 2 WHERE ROUND = 3")

    cur.execute("UPDATE Tur SET GOALS1 = 0 WHERE ROUND = 4")
    cur.execute("UPDATE Tur SET GOALS2 = 2 WHERE ROUND = 4")

    con.commit()
    con.close()

    db_add_stats(1, 'Tur')
    db_add_stats(2, 'Tur')
    db_add_stats(3, 'Tur')
    db_add_stats(4, 'Tur')

    con = db_connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM Teams")
    all_rows = cur.fetchall()

    new_list_1 = (list(all_rows[0]))[2:]
    new_list_2 = (list(all_rows[1]))[2:]
    new_list_3 = (list(all_rows[2]))[2:]
    new_list_4 = (list(all_rows[3]))[2:]
    new_list_5 = (list(all_rows[4]))[2:]
    new_list_6 = (list(all_rows[5]))[2:]
    new_list_7 = (list(all_rows[6]))[2:]
    new_list_8 = (list(all_rows[7]))[2:]
    new_list_9 = (list(all_rows[8]))[2:]
    new_list_10 = (list(all_rows[9]))[2:]

    assert new_list_1 == team1
    assert new_list_2 == team2
    assert new_list_3 == team3
    assert new_list_4 == team4
    assert new_list_5 == team5
    assert new_list_6 == team6
    assert new_list_7 == team7
    assert new_list_8 == team8
    assert new_list_9 == team9
    assert new_list_10 == team10