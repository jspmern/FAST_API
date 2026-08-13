import json
#this function is used to read the data from the json file and return the data in json format
def read_json():
    with open("asset/data.json","r" ) as f:
        try:
            data=json.load(f)
            return data
        except json.JSONDecodeError:
            return {"error": "Invalid JSON in data file"}