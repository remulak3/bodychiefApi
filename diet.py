from datetime import date, datetime, timedelta
import http.client
import json
import sys

helpMessage = """
    Available commands are:
    1.help - for getting this informations.
    2.diets - for listing available diets. 
    3.plan {dietId} - for listing meals for diet selected.
    4.plan {dietId} week - for listing meals for diet selected for next 7 days
    """

def downloadData():
    conn = http.client.HTTPSConnection("webapi.bodychief.pl")
    payload = json.dumps({
    "lang": "pl",
    "data": {
        "city_id": 1
    }
    })
    headers = {
    'Content-Type': 'application/json'
    }
    conn.request("POST", "/bodychief_api/getMenu", payload, headers)
    res = conn.getresponse()
    data = res.read()
    decodedData = data.decode("utf-8")
    jsonData = json.loads(decodedData)
    return jsonData['value']

def setDietDateToToday(delta = 0):
    today = date.today()
    if delta > 0:
        today = today + timedelta(days = delta)       
    return str(today)

def getDietTypes():
    today = setDietDateToToday()
    data = downloadData()
    dietIds = {}
    for id in data[today]['menu_d'].items():
        dietId = id[0]
        dietName = id[1]['name']
        dietIds[dietName] = dietId
    for name, id in dietIds.items():
        print(name, id)

def printDishesForDateAndDiet(date, dietId):
    data = downloadData()
    dietInfo = data[date]['menu_d'][dietId]

    print("### " + dietInfo['name'] + " ###")
    for dish in dietInfo['menu_c']:
        print("# " + dish['name'])
        print(dish['dish'])

def getDietPlanForWeek(dietId):
    for day in range(7):
        currentDay = setDietDateToToday(day)
        print("## Current Day: " + currentDay)
        printDishesForDateAndDiet(currentDay, dietId)

def main(argv):
    defaultDietId = "id9"
    selectedDietId = defaultDietId

    if (len(argv) < 2 or argv[1] == "help"):
        print(helpMessage)
        
    elif (argv[1] == "diets"):
        getDietTypes()
    
    elif (argv[1] == "plan"):
        if (len(argv) > 1):
            selectedDietId = argv[2]
        if (len(argv) > 2):
            getDietPlanForWeek(selectedDietId)
        else:
            today = setDietDateToToday()
            printDishesForDateAndDiet(today, selectedDietId)
    else:
        print("Wrong argument, displaying avalible arguments")
        print(helpMessage)

if __name__ == "__main__":
    main(sys.argv)


        
    


    



