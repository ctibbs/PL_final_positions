##Script to extract and analyse all of Premier League tables
##All statistics extracted from https://en.wikipedia.org/wiki/2004%E2%80%9305_Premier_League
##
##Usage: >python premier_league_tables.py <PL team>
##
##Usage (interactive): >python -i premier_league_tables.py <PL team>
##
##Written by C. Tibbs (Nov 2022)
##

##Import Python packages
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import json
import datetime
import calendar
import sys
from http import HTTPStatus
from pathlib import Path
from bs4 import BeautifulSoup
import py_local_settings

##Define paths and filenames
path = Path(py_local_settings.python_path+'\\Premier_League\\Wikipedia\\')

##Identify the team
PL_team = sys.argv[1]

##Define parameters
PL_positions = {}

##Define the URLs and loop over years
PL_years = range(1992, 2022, 1)
for PL_year in PL_years:
    print('Analysing the '+str(PL_year)+'-'+str(PL_year+1)+' season...')
    PL_year_url_str = str(PL_year)+'%E2%80%93'+str(PL_year+1)[2:]
    url = 'https://en.wikipedia.org/wiki/'+PL_year_url_str+'_Premier_League'
    
    ##Request the webpage from the URL
    r = requests.get(url)

    ##Check if call was unsuccessful
    if r.status_code != HTTPStatus.OK:
        print('Problem with this call...')

    ##Check if call was successful
    elif r.status_code == HTTPStatus.OK:

        ##Parse the data
        bs_r = BeautifulSoup(r.text, 'html.parser')
    
        ##Find the league tables
        table = bs_r.find_all('table', {'class':'wikitable', 'style':'text-align:center;'})

        ##Convert the data table to DataFrames
        df = pd.read_html(str(table))
        df = pd.DataFrame(df[0])
       
        ##Identify column containing the teams
        ##(this is required as there is an issue with the column name for one year)
        m=df.columns[df.columns.str.contains('Team')][0]

        ##Update the column containg teams to "Team"
        df.rename(columns={m: 'Team',}, inplace=True)

        ##Remove any NANs in the "Team" column
        df = df.dropna(subset='Team')

        ##Check that the team was in the PL this year
        team_exists = df[df['Team'].str.startswith(PL_team)]

        if len(team_exists) == 1:
            ##Extract team position and collate into dictionary
            PL_positions[PL_year+1] = int(df[df['Team'].str.startswith(PL_team)]['Pos'])
        else:
            ##Add NAN value for position
            PL_positions[PL_year+1] = float('nan')

##Plot the PL positions
plt.title(PL_team+' Premier League Table Positions')
plt.xlabel('Season')
plt.ylabel('Final League Position')
plt.grid(True)
plt.xticks(list(PL_positions.keys()), list(PL_positions.keys()), rotation='vertical')
plt.ylim(max(PL_positions.values()),1)
plt.plot(PL_positions.keys(), PL_positions.values(), 'o--r')
plt.savefig(path.joinpath('Final_PL_League_Table_Positions_'+PL_team+'.pdf'))
plt.clf()

























    

        
