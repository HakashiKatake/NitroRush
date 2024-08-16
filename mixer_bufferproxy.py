import json
from lib_misc import *

data_json = []

with open("Json_datafile.json", 'r') as f:
  data_json = json.load(f)

def save():
    with open("Json_datafile.json", 'w') as f:
        json.dump(data_json, f, indent=2)






def database_update(section, action, value=None):
    global data_json
    nan = True
    if value != None and section != "ability" and section != "color" and section != "Owned_Skills" and section != "ability_level":
        value = int(value)
        nan = False
    if section == "highscore":
        index = 0
    if section == "coins":
        index = 1
    if section == "ability":
        index = 2
    if section == "color":
        index = 3
    if section == "Owned_Skills":
        index = 4 
    if section == "ability_level":
        index = 5
    if action == "add":
        data_json[index] += value
    if action == "sub":
        data_json[index] -= value
    if action == "view":
        if action == "view" and section == "coins" or section == "highscore":
            return decrypt(data_json[index])
        else:
            return data_json[index]
    if action == "equals":
        data_json[index] = value
    if action == "equals" and section == "coins" or section == "highscore":
        data_json[index] = crypt(value)
    else:
        data_json[index] = value
    save() 



        