import os, sys, glob
import datetime 

def find_file(file):
    """
    Find correct save file
    """
    res = glob.glob(f"**/{file}", recursive=True)
    return res[0]

def get_day():
    """
    x-axis boundary moment
    """
    today = datetime.datetime.utcnow().date()
    end_x = (today + datetime.timedelta(days=1))
    return end_x