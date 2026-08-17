import string

from fastapi import FastAPI
from utilis import read_json, write_json
from pydantic import BaseModel
#initialize the FastAPI app
app = FastAPI()


#this is a health check endpoint to check if the application is running or not and we can run by uvicorn main:app --reload and we can check swagger document at localhost:8000/docs
@app.get("/health")
async def health_check():
    return {"success":True,"message":"Application is up and running at 8000"}

#get all employee details
@app.get("/")
async def get_all_employee_details():
    data= read_json()
    try:
        if "error" in data:
            return {"success":False,"message":data["error"]}
        return {"success":True,"data":data}
    except Exception as e:
        return {"success":False,"message":str(e)}

#create pydentic class for employee details
class Employee (BaseModel):
    name:str
    age:int
    department:str
    salary:float
    position:str

# create a new employee 
@app.post('/')
async def create_emp(emp:Employee):
    try:
        data = write_json(emp)
        if isinstance(data, dict) and "error" in data:
            return {"success": False, "message": data["error"]}

        return {"success": True, "message": "Employee created successfully", "data": data}
    except Exception as e:
        return {"success": False, "message": str(e)}
