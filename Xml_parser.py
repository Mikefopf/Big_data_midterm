import xml.etree.cElementTree as ET
import pandas as pd
tree = ET.parse('PointzAggregator-AirlinesData.xml')
root = tree.getroot()

cols = ["uid", "First name", "Last name", "Card type", "Bonusprogramm", "Activity type", "Flight code", "Date", "Departure", "Arrival", "Fare"]
rows = []

for user in root.findall('user'):
    uid = user.get('uid')
    name = user.find('name').attrib
    #print(name)
    firstName = name['first']
    lastName = name['last']
    #print(firstName + ' ' + lastName)
    for cards in user.findall('cards'):
        cardsType = cards.get('type')
        #print(cardsType)
        for card in cards.findall('card'):
            bonusprogramm = card.find('bonusprogramm').text
            #print(bonusprogramm.text)
            for activities in card.findall('activities'):
                activitiesType = activities.get('type')
                #print(activitiesType)
                for activity in activities.findall('activity'):
                    Code = activity.find('Code').text
                    Date = activity.find('Date').text
                    Departure = activity.find('Departure').text
                    Arrival = activity.find('Arrival').text
                    Fare = activity.find('Fare').text
                    rows.append({"uid": uid, 
                                 "First name": firstName, 
                                 "Last name": lastName, 
                                 "Card type": cardsType, 
                                 "Bonusprogramm": bonusprogramm, 
                                 "Activity type": activitiesType, 
                                 "Flight code": Code, 
                                 "Date": Date, 
                                 "Departure": Departure, 
                                 "Arrival": Arrival, 
                                 "Fare": Fare})


df = pd.DataFrame(rows, columns=cols)
  
# Writing dataframe to csv
df.to_csv('PointzAggregator-AirlinesDate2.csv')
                    
