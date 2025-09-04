from db.db import *
import pandas as pd
import bs4 as bs
import requests
from school_naming_information import *

YEAR = 2025
URLS = {
    "schedule": f"https://www.sports-reference.com/cfb/years/{YEAR}-schedule.html",
    "team_offense": f"https://www.sports-reference.com/cfb/years/{YEAR}-team-offense.html",
    "team_defense": f"https://www.sports-reference.com/cfb/years/{YEAR}-team-defense.html",
    "team_special_teams": f"https://www.sports-reference.com/cfb/years/{YEAR}-special-teams.html"
}

def check_url(url: str) -> bool:
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False


#[Winner, Loser, Winner_Points, Loser_Points, Location, Date, Time, Day, Week, Year, Month, Day, winner_id, loser_id]
def fetch_schedule(YEAR: int):
    URL = f"https://www.sports-reference.com/cfb/years/{YEAR}-schedule.html"        
    if check_url(str(URL)):
        print(f"Successfully fetched schedule")
    else:
        print(f"Failed to fetch schedule")
        return None
   
    # Fetch the actual HTML content
    response = requests.get(URL)
    soup = bs.BeautifulSoup(response.text, features="html.parser")
    soup = soup.find_all("table", {"id": "schedule"})
    headers = soup[0].find_all("th")
    headers = [header.text for header in headers]
    
    #remove duplicates and int
    headers = headers[1:10]
    headers_pts_index = headers.index("Pts")
    headers[headers_pts_index] = "Winner Points"
    headers_pts_index = headers.index("Pts")
    headers[headers_pts_index] = "Loser Points"
    headers_locations_index = headers.index("")
    headers[headers_locations_index] = "Location"



    data = soup[0].find_all("tr")
    data = data[1:]
    data_dict = {}
    headers[0] = "Week"
    for header in headers:
        data_dict[header] = []
    data_dict["Year"] = []
    data_dict["Month"] = []
    data_dict["Day"] = []
    data_dict["Winner ID"] = []
    data_dict["Loser ID"] = []
    
    for row in data:
        row_data = row.find_all("td")
        row_data = [data.text for data in row_data]
        if len(row_data) != 0:
            Winner_Score = row_data[5]
            Loser_Score = row_data[8]
            if Winner_Score == "" and Loser_Score == "":
                continue
            elif Winner_Score == "0" or Loser_Score == "0":
                continue
            else:
                print(headers)
                print(row_data[:len(headers)])
                Week = row_data[0]
                Date = row_data[1]
                Time = row_data[2]
                Day = row_data[3]
                Winner_team = row_data[4]
                Winner_team_points = row_data[5]
                Location = row_data[6]
                Loser_team = row_data[7]
                Loser_team_points = row_data[8]
                try:
                    Winner_team_rank_index = Winner_team.index(")")
                except:
                    Winner_team_rank_index = None
                try:
                    Loser_team_rank_index = Loser_team.index(")")
                except:
                    Loser_team_rank_index = None
                if Winner_team_rank_index is not None:
                    Winner_team = Winner_team[Winner_team_rank_index+2:]
                if Loser_team_rank_index is not None:
                    Loser_team = Loser_team[Loser_team_rank_index+2:]

                data_dict["Winner"].append(Winner_team)
                data_dict["Loser"].append(Loser_team)
                data_dict["Winner Points"].append(Winner_team_points)
                data_dict["Loser Points"].append(Loser_team_points)
                data_dict["Location"].append(Location)
                data_dict["Date"].append(Date)
                data_dict["Time"].append(Time)
                data_dict["Day"].append(Day)
                data_dict["Week"].append(Week)
                date_split = Date.split(" ")
                Year = date_split[2]
                Month = month_number_from_month_abbreviation(date_split[0])
                Day = date_split[1]
                data_dict["Year"].append(Year)
                data_dict["Month"].append(Month)
                data_dict["Day"].append(Day)
                _, _, winner_id = get_school_naming_infomation(Winner_team)
                _, _, loser_id = get_school_naming_infomation(Loser_team)
                data_dict["Winner ID"].append(winner_id)
                data_dict["Loser ID"].append(loser_id)

        else:
            continue

    return data_dict


def fetch_and_store_schedule(year):
    data_dict = fetch_schedule(year)
    CONN = connect_to_db("db/schools.db")
    insert_data_into_table(CONN, data_dict, "schedule")
    close_connection(CONN)


