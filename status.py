from fastapi import FastAPI,status
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