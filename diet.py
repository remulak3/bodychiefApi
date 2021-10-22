'''
Module for downloading and operating diet information using
bodychief API

'''

from datetime import date, timedelta
import http.client
import json
import sys

HELP_MESSAGE = """
    Available commands are:
    1.help - for getting this informations.
    2.diets - for listing available diets. 
    3.plan {diet_id} - for listing meals for diet selected.
    4.plan {diet_id} week - for listing meals for diet selected for next 7 days
    """

def download_data():
    '''Downloads diet information by doing API call.'''

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
    decoded_data = data.decode("utf-8")
    json_data = json.loads(decoded_data)
    return json_data['value']

def set_diet_date_to_today(delta = 0):
    '''Returning date string with optional offset in days.'''
    today = date.today()
    if delta > 0:
        today = today + timedelta(days = delta)
    return str(today)

def get_diet_types():
    '''Printing available diet types.'''
    today = set_diet_date_to_today()
    data = download_data()
    diet_ids = {}
    for menu_id in data[today]['menu_d'].items():
        diet_id = menu_id[0]
        diet_name = menu_id[1]['name']
        diet_ids[diet_name] = diet_id
    for name, diet_id in diet_ids.items():
        print(name, diet_id)

def print_dishes_for_date_and_diet(selected_date, diet_id):
    '''Printing meals for specified day an diet_id.'''
    data = download_data()
    diet_info = data[selected_date]['menu_d'][diet_id]

    print("### " + diet_info['name'] + " ###")
    for dish in diet_info['menu_c']:
        print("# " + dish['name'])
        print(dish['dish'])

def get_diet_plan_for_week(diet_id):
    '''Printing plan for specified diet_id for the whole week.'''
    for day in range(7):
        current_day = set_diet_date_to_today(day)
        print("## Current Day: " + current_day)
        print_dishes_for_date_and_diet(current_day, diet_id)

def main(argv):
    '''Provides information about diet from bodychief.'''
    defaultdiet_id = "id9"
    selecteddiet_id = defaultdiet_id

    if (len(argv) < 2 or argv[1] == "help"):
        print(HELP_MESSAGE)
    elif argv[1] == "diets":
        get_diet_types()
    elif argv[1] == "plan":
        if len(argv) > 1:
            selecteddiet_id = argv[2]
        if len(argv) > 2:
            get_diet_plan_for_week(selecteddiet_id)
        else:
            today = set_diet_date_to_today()
            print_dishes_for_date_and_diet(today, selecteddiet_id)
    else:
        print("Wrong argument, displaying avalible arguments")
        print(HELP_MESSAGE)

if __name__ == "__main__":
    main(sys.argv)
