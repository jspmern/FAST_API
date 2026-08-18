#this is for learning all about pydantic validatior
from fastapi import FastAPI
from pydantic import BaseModel,Field,field_validator
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
# class Emp(BaseModel):
#     name:str
#     # id:int=1 #if not provide it take as a defult value  :👉 i want id always be a postive no
#     id:int=Field(
#         ge=0
#     )
#     address:str |None=None   #make it optional
# @app.post('/')
# def createEmp(Emp:Emp):
#     employee.append(Emp)
#     return employee



#nested modal
class Emp(BaseModel):
    name:str|None=None
    age:int=Field(ge=0,le=100)
    password:str

    @field_validator('password')
    @classmethod
    def validate_password(cls,value):
        if len(value)<8:
            raise ValueError("password must contain at 8 character")
        return value
class EmpDetails(BaseModel):
    company:str
    employeeDetails:Emp

# here i am going to impliment response model that is good for senitization 
class EmpResDetails(BaseModel):
    company:str


@app.post('/',response_model=EmpResDetails)
def createEmp(emp:EmpDetails):
    employee.append(emp)
    return emp        
