from fastapi import FastAPI,status,HTTPException
#creating the app 
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

#testing health
@app.get('/')
def gethealth():
    return {"status":"ok"}

#send status code manually
@app.get('/user',status_code=status.HTTP_201_CREATED)
def getUser():
    return employee

#http expection also we can send form fast api
@app.get('/studend/{id}')
def getstudentData(id:str):
    if id=="utsav":
        raise HTTPException(status_code=404,detail="this user is not allowed")
    return employee