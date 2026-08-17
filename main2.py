#this is for learning all about pydantic validatior
from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()
#dummy employee for learn pydantic
employee=[
    {
    "name":"utsav",
    "id":1
    },
    {
    "name":"vijaya",
    "id":2
    },
    {
    "name":"aman",
    "id":3
    },

]

#for fetch all employee details
@app.get('/')
def getUser():
    return employee

#for create new employee
# @app.post('/')
# def createEmp(Emp:dict):
#     employee.append(Emp)
#     return employee

#note 👉 as you see write now can add any sort of data for validation of request data we need pydantic

#this both field is requrie
class Emp(BaseModel):
    name:str
    id:int 
    address:str |None=None   #make it optional
@app.post('/')
def createEmp(Emp:Emp):
    employee.append(Emp)
    return employee

