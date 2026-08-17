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
#this is the pydantic class for edit the employee
class EmployeeEdit(BaseModel):
    newName:str
    name:str

#update the employee
@app.put('/')
async def edit_employee(emp:EmployeeEdit):
    try:
        data=read_json()
        for item in data:
            if item["name"] == emp.name:
                item["name"] = emp.newName
                updated = True
                break

        if not updated:
            return {
                "success": False,
                "message": "Employee not found"
            }  
        write_json(data)
        return {"success":True,"message":"Employee updated successfully"}
    except Exception as e:
        return {"success":False ,"message":str(e)}


#read query String  

# # required query parameter for department  
# @app.get("/employees")
# def get_employees(department: str):

#optional query parameter for department
# @app.get("/employees")
# def get_employees(
#     department: str | None = None
# ):    

@app.get('/search')
async def get_employee_by_query(skip:int=0, limit:int=10, name:str=None):
    print(skip, limit, name)
    try:
        print(skip, limit, name)
        return {"success": True, "message":f"{skip} {limit} {name}"}
    except Exception as e:
        return {"success": False, "message": str(e)}

#read path parameter 
@app.get('/{name}')
async def get_employee_by_name(name:str):
    try:
        data=read_json()
        for item in data:
            if item["name"] == name:
                return {"success":True,"data":item}
        return {"success":False,"message":"Employee not found"}
    except Exception as e:
        return {"success":False,"message":str(e)}    

