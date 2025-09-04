from db.db import *
import pandas as pd
import time
try:
    CONN = connect_to_db("db/schools.db")
except:
    conn = connect_to_db("db\\schools.db")

def calculate_margin_of_victory_score(Winning_Team_Points, Losing_Team_Points):
    margin_of_victory = Winning_Team_Points - Losing_Team_Points
    margin_of_victory_score = 0
    if margin_of_victory <= 3:
        margin_of_victory_score = 0.5
    elif margin_of_victory <= 10:
        margin_of_victory_score = 1
    elif margin_of_victory <= 17:
        margin_of_victory_score = 2
    elif margin_of_victory <= 24:
        margin_of_victory_score = 4
    elif margin_of_victory <= 31:
        margin_of_victory_score = 5
    elif margin_of_victory <= 38:
        margin_of_victory_score = 6
    elif margin_of_victory <= 45:
        margin_of_victory_score = 7
    else:
        margin_of_victory_score = 8

    return margin_of_victory_score


def calculate_running_rankings(year: int) -> dict:
    start_time = time.time()
    dict_data = query_db(CONN, f"SELECT * FROM schedule where Year = {year} and Month >= 8 or Year = {year+1} and Month < 8")


    running_rankings = {}

    for i in range(0,len(dict_data["Winner"])):
        Winning_Team = dict_data["Winner"][i]
        Losing_Team = dict_data["Loser"][i]
        Winning_Team_Points = dict_data["Winner Points"][i]
        Losing_Team_Points = dict_data["Loser Points"][i]

        margin_of_victory_score = calculate_margin_of_victory_score(Winning_Team_Points, Losing_Team_Points)
        
        if Winning_Team not in running_rankings:
            running_rankings[Winning_Team] = 0
        if Losing_Team not in running_rankings:
            running_rankings[Losing_Team] = 0

        running_rankings[Winning_Team] += margin_of_victory_score
        running_rankings[Losing_Team] -= margin_of_victory_score

    

    end_time = time.time()
    
    time_taken = end_time - start_time
    time_taken_ms = time_taken * 1000
    print(f"Time taken: {time_taken_ms} milliseconds")
    return running_rankings

def calculate_rankings_with_previous_year(year: int, running_rankings: dict) -> dict:
    start_time = time.time()
    dict_data = query_db(CONN, f"SELECT * FROM schedule where Year = {year} and Month >= 8 or Year = {year+1} and Month < 8")
    running_rankings_copy = running_rankings.copy()

    for i in range(0,len(dict_data["Winner"])):
        Winning_Team = dict_data["Winner"][i]
        Losing_Team = dict_data["Loser"][i]
        Winning_Team_Points = dict_data["Winner Points"][i]
        Losing_Team_Points = dict_data["Loser Points"][i]

        margin_of_victory_score = calculate_margin_of_victory_score(Winning_Team_Points, Losing_Team_Points)
        

        if Winning_Team not in running_rankings_copy:
            running_rankings_copy[Winning_Team] = 0
        if Losing_Team not in running_rankings_copy:
            running_rankings_copy[Losing_Team] = 0

        running_rankings_copy[Winning_Team] += margin_of_victory_score
        running_rankings_copy[Losing_Team] -= margin_of_victory_score


    end_time = time.time()
    time_taken = end_time - start_time
    time_taken_ms = time_taken * 1000
    print(f"Time taken: {time_taken_ms} milliseconds")
    
    return running_rankings_copy



