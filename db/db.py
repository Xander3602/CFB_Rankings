"""
Summary: This file contains the database connection along with functions to interact with the sqlite database.

Author: Xander Lowry
Date-Created: 2024-09-30
Date-Latest-Update: 2024-10-10
"""
#IMPORTS
import sqlite3
import os
import pandas as pd

def connect_to_db(db_name: str) -> sqlite3.Connection:
    """_summary_
    Connects to the sqlite database with the given name.
    Args:
        db_name (str): Name of the database to connect to.

    Returns:
        sqlite3.Connection: sqlite3 connection object for the database.
    """
    try:
        conn = sqlite3.connect(f"{os.getcwd()}/{db_name}")
        return conn
    except sqlite3.Error as e:
        print(e)
        return None


def create_table(conn: sqlite3.Connection, column_names: list, table_name: str) -> None:
    """_summary_
    Creates a table in the database with the given column names wuth the given table name from the given connection.
    Args:
        conn (sqlite3.Connection): sqlite3 connection object for the database.
        column_names (list): List of column names for the table.
        table_name (str): Name of the table to create.
    """
    try:
        c = conn.cursor()
        # Quote column names to handle spaces and special characters
        columns = ', '.join([f'"{name}"' for name in column_names])
        c.execute(f"CREATE TABLE {table_name} ({columns})")
    except sqlite3.Error as e:
        print(e)
        
def insert_data_into_table(conn: sqlite3.Connection, data_dic: dict, table_name: str) -> None:
    """_summary_
    Inserts the given DataFrame into the given table in the database using the given connection.
    Args:
        conn (sqlite3.Connection): sqlite3 connection object for the database.
        df (pd.DataFrame): DataFrame to insert into the table.
        table_name (str): Name of the table to insert the data into.
    """
    try:
        c = conn.cursor()
        # Quote column names to handle spaces and special characters
        columns = ', '.join([f'"{key}"' for key in data_dic.keys()])
        
        for i in range(len(data_dic[list(data_dic.keys())[0]])):
            # Prepare values, handling NaN and special characters
            value_list = []
            for key in data_dic.keys():
                value = data_dic[key][i]
                if pd.isna(value):  # Handle NaN values
                    value_list.append('NULL')
                elif isinstance(value, str):
                    # Escape single quotes by doubling them
                    escaped_value = value.replace("'", "''")
                    value_list.append(f"'{escaped_value}'")
                else:
                    value_list.append(str(value))
            
            values = ', '.join(value_list)
            try:
                c.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")
            except sqlite3.Error as e:
                print(f"Error inserting row {i}: {e}")
                continue
        
        conn.commit()
        print(f"Successfully inserted {len(data_dic[list(data_dic.keys())[0]])} rows")
        
    except Exception as e:
        print(f"Error in insert_data_into_table: {e}")
        conn.rollback()
    
    
    # except sqlite3.Error as e:
    #     print(e)
    

def query_db(conn: sqlite3.Connection, query: str) -> dict:
    """_summary_
    Queries the database with the given query using the given connection.
    Args:
        conn (sqlite3.Connection): sqlite3 connection object for the database.
        query (str): Query to execute on the database.

    Returns:
        pd.DataFrame: DataFrame containing the results of the query.
    """
    try:
        c = conn.cursor()
        result = c.execute(query)
        rows = result.fetchall()
        columns = [description[0] for description in c.description] 
        dict_data = {}
        for i, column in enumerate(columns):
            for row in rows:
                if column not in dict_data:
                    dict_data[column] = []
                dict_data[column].append(row[i])
        return dict_data
    except sqlite3.Error as e:
        print(e)
        return None
    except Exception as e:
        print(e)
        return None
    
def get_last_row(conn: sqlite3.Connection, table_name: str) -> dict:
    """_summary_
    Gets the last row of the given table in the database using the given connection.
    Args:
        conn (sqlite3.Connection): sqlite3 connection object for the database.
        table_name (str): Name of the table to get the last row from.

    Returns:
        pd.DataFrame: DataFrame containing the last row of the table.
    """
    try:
        c = conn.cursor()
        c.execute(f"SELECT * FROM {table_name} ORDER BY ROWID DESC LIMIT 1")
        row = c.fetchone()
        dict_data = {0: row}
        return dict_data
    except sqlite3.Error as e:
        print(e)
        return None

def get_length_of_table(conn: sqlite3.Connection, table_name: str) -> int:
    """_summary_
    Gets the length of the given table in the database using the given connection.
    Args:
        conn (sqlite3.Connection): sqlite3 connection object for the database.
        table_name (str): Name of the table to get the length of.

    Returns:
        int: Number of rows in the table.
    """
    try:
        c = conn.cursor()
        c.execute(f"SELECT COUNT(*) FROM {table_name}")
        return c.fetchone()[0]
    except sqlite3.Error as e:
        print(e)
        return None

def close_connection(conn: sqlite3.Connection) -> None:
    """_summary_
    Closes the connection to the database.
    Args:
        conn (sqlite3.Connection): sqlite3 connection object for the database.
    """
    try:
        conn.close()
    except sqlite3.Error as e:
        print(e)
        

def db_info(conn: sqlite3.Connection) -> None:
    """_summary_
    Prints the schema of the database.
    Args:
        conn (sqlite3.Connection): sqlite3 connection object for the database.
    """
    try:
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = c.fetchall()
        for table in tables:
            print(f"Table: {table[0]}")
            c.execute(f"PRAGMA table_info({table[0]})")
            columns = c.fetchall()
            for column in columns:
                print(f"    {column[1]}")
    except sqlite3.Error as e:
        print(e)