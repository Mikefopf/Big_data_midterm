import yaml
import pandas as pd

cols = ["Passanger", "Date", "Fligth code", "Departure", "Arrival", "Class", "Fare"]
rows = []

key = 1
allData = []
for i in range(340, 366):
    with open('xx' + str(i), 'r') as f:
        data = yaml.safe_load(f)
        for date in data:
            #print(date)
            for fligth in data[date]:
                #print(fligth)
                Departure = data[date][fligth]['FROM']
                Arrival = data[date][fligth]['TO']
                Status = data[date][fligth]['STATUS']
                for Passanger in data[date][fligth]['FF']:
                    Class = data[date][fligth]['FF'][Passanger]['CLASS']
                    Fare = data[date][fligth]['FF'][Passanger]['FARE']
                    rows.append({"Passanger": Passanger, 
                                 "Date": date, 
                                 "Fligth code": fligth,  
                                 "Departure": Departure, 
                                 "Arrival": Arrival, 
                                 "Status": Status, 
                                 "Class": Class, 
                                 "Fare": Fare})                
df = pd.DataFrame(rows, columns=cols)
  
# Writing dataframe to csv
df.to_csv('SkyTeam-Exchange12.csv') 