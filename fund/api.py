# necessary imports
import os, sys, glob
from pathlib import Path
import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
path = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(path)

def find_file(dir):
    """
    Find correct save file
    """
    include = ["fund-vis-v2", "saved"]
    ret = ''
    for root, dirs, files in os.walk(dir):
        dirs[:] = [d for d in dirs if d in include]
        for names in files:
            if names.endswith('.csv'):
                # print(os.path.join(root, names))
                ret = os.path.join(root, names)
    return ret

# print(sys.platform)
CWD = os.getcwd()
# print(type(CWD))
SF_NAME = "temp.csv" # change when needed 
cwd_path = Path(CWD)
PARENT = str(cwd_path.parent.absolute()) # docs/tonk
# print(PARENT)
SAVEFILE = find_file(PARENT)
# print(SAVEFILE)

URL = "https://tankionline.com/pages/summer-major/?lang=en" # change when needed
START_DATE = datetime.datetime.strptime("2022-07-04 2:00", "%Y-%m-%d %H:%M")
CHECKPOINTS = {1: "Nuclear Energy", 4: "Prot Slot", 7: "Skin Container", 8: "Magnetic Pellets", 9: "Helios", 10: "Hammer LGC", 11: "Vacuum Shell", 12: "Swarm", 13: "Pulsar", 14: "Armadillo", 15: "Crisis"}

# stealing my old code
def scrape(checkstatus=False):
    try: 
        page = requests.get(URL, timeout=(5, 15))
        soup = BeautifulSoup(page.content, "html.parser")
        fund = soup.find_all("span", class_="ms-3")
        fund_text = fund[0].text
        if checkstatus:
            return "Up to date"
    except:
        fund_text = pd.read_csv(SAVEFILE).iloc[-1, 1]
        if checkstatus:
            return "Being DDoS'ed again"
    return datetime.datetime.utcnow(), fund_text

# temp strat for plotly
def write_to_csv():
    with open(SAVEFILE, "a") as f:
        time, fund = scrape()
        fund = fund.replace(",", "")
        time = time.strftime('%Y-%m-%d %H:%M')
        f.write(f"{time},{fund}\n")