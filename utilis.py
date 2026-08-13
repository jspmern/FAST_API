import json
#this function is used to read the data from the json file and return the data in json format
def read_json():
    with open("asset/data.json","r" ) as f:
        try:
            data=json.load(f)
            return data
        except json.JSONDecodeError:
            return {"error": "Invalid JSON in data file"}

#this is a function to write the data to the json file and return the data in json format
def write_json(data):
    with open ("asset/data.json","w" ) as f:
        try:
            json.dump(data,f,indent=4)
            return data
        except Exception as e:
            return {"error": str(e)}