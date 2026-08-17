import json

#this function is used to read the data from the json file and return the data in json format
def read_json():
    try:
        with open("asset/data.json", "r") as f:
            data = json.load(f)
            if data is None:
                return []
            if isinstance(data, list):
                return data
            return [data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

#this is a function to write the data to the json file and return the data in json format
def write_json(data):
    try:
        read_data = read_json()
        if not isinstance(read_data, list):
            read_data = [read_data]

        employee_data = data.dict() if hasattr(data, "dict") else data
        read_data.append(employee_data)

        with open("asset/data.json", "w") as f:
            json.dump(read_data, f, indent=4)

        return employee_data
    except Exception as e:
        return {"error": str(e)}