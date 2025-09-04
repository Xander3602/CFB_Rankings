import requests
from db.db import *
import pandas as pd

def download_college_names_file(url, filename="names.txt"):
    """
    Saves the college names file to the current directory.

    File comes from https://talismanred.com/ratings/cf/wilson/names.txt 

    Args:
        url: The URL of the college names file.
        filename: The name of the file to save the college names to. Defaults to "names.txt".
    """
    response = requests.get(url)
    with open(filename, "w") as f:
        f.write(response.text)
