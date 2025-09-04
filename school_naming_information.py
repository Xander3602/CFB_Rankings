from db.db import *
import os
import pandas as pd


def month_number_from_month_abbreviation(month_abbreviation: str) -> int:
    """_summary_
    Gets the month number from the month abbreviation.
    Args:
        month_abbreviation (str): Abbreviation of the month to get the number for.
    """
    months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    if type(month_abbreviation) != str:
        raise ValueError(f"Invalid type for month abbreviation: {type(month_abbreviation)}, expected str")
    if month_abbreviation.lower() not in months:
        raise ValueError(f"Invalid month abbreviation: {month_abbreviation}, expected one of {months}")
    
    months = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}
    return months[month_abbreviation.lower()]

def get_school_naming_infomation(school_name):
    """_summary_
    Gets the naming infomation for the given school name.
    Args:
        school_name (str): Name of the school to get the naming infomation for.

    Returns:
        tuple: Tuple containing the canonical name, aliases, and ID of the school in that order. Should return None if the school is not found.

    """
    # Try different possible paths for the database
    possible_paths = [
        "db/schools.db",  # When called from root directory
        "../db/schools.db",  # When called from testing directory
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "db", "schools.db")  # Absolute path
    ]
    
    conn = None
    for db_path in possible_paths:
        try:
            conn = connect_to_db(db_path)
            if conn is not None:
                break
        except Exception:
            continue
    
    if conn is None:
        return None
    query_canonical_name = f'SELECT * FROM schools WHERE "Canonical Name" = \'{school_name}\''
    query_aliases = f'SELECT * FROM schools WHERE "Aliases" LIKE \'%{school_name}%\''

    naming_infomation = query_db(conn, query_canonical_name)
    if naming_infomation is None or len(naming_infomation.get('ID', [])) == 0:
        naming_infomation = query_db(conn, query_aliases)
        if naming_infomation is None or len(naming_infomation.get('ID', [])) == 0:
            print(f"No school found with canonical name or aliases '{school_name}'")
            return None

    canonical_name = naming_infomation['Canonical Name'][0]
    if naming_infomation['Aliases'][0] is None:
        aliases = []
    else:
        aliases = naming_infomation['Aliases'][0].split(",")
        aliases = [alias for alias in aliases if alias != " "]
    ID = naming_infomation['ID'][0]

    close_connection(conn)
    return canonical_name, aliases, ID

def update_schedule_with_ID_information():
    """_summary_
    Updates the schedule with the ID information for the schools.
    """
    try:
        schedule = pd.read_csv("data/schedule.csv")
    except Exception as e:
        schedule = pd.read_csv("data\\schedule.csv")

    schedule.drop(columns=["Rk","Notes"], inplace=True)
    schedule.rename(columns={"Unnamed: 7":"Location"}, inplace=True)
    schedule.rename(columns={"Wk":"Week"}, inplace=True)
    schedule.rename(columns={"Pts": "Winner Points","Pts.1": "Loser Points"}, inplace=True)

    updated_schedule_df = pd.DataFrame(columns=["Winner", "Loser", "Winner Points", "Loser Points", "Location", "Date", "Time", "Day", "Week", "Year", "Month", "Day", "Winner ID", "Loser ID"])

    for index, row in schedule.iterrows():
        Winner = row["Winner"]
        Loser = row["Loser"]

        if Winner[0] == "(":
            find_index = Winner.find(")")
            Winner = Winner[find_index+2:]
        if Loser[0] == "(":
            find_index = Loser.find(")")
            Loser = Loser[find_index+2:]

        Winner_Points = row["Winner Points"]
        Loser_Points = row["Loser Points"]
        Location = row["Location"]
        Date = row["Date"]
        Time = row["Time"]
        Day = row["Day"]
        Week = row["Week"]
        _, _, winner_id = get_school_naming_infomation(Winner)
        _, _, loser_id = get_school_naming_infomation(Loser)
        
        Date = row["Date"]
        date_parts = Date.split(" ")
        Year = date_parts[2]
        Month = month_number_from_month_abbreviation(date_parts[0])
        Day = date_parts[1]


        updated_schedule_df.loc[index] = [Winner, Loser, Winner_Points, Loser_Points, Location, Date, Time, Day, Week, Year, Month, Day, winner_id, loser_id]
    dict_data = updated_schedule_df.to_dict(orient="list")

    try:
        conn = connect_to_db("db/schools.db")
    except:
        conn = connect_to_db("db\\schools.db")

    create_table(conn, dict_data.keys(), "schedule")
    insert_data_into_table(conn, dict_data, "schedule")
    close_connection(conn)

