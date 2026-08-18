from fastapi import FastAPI,Depends,Header,HTTPException,Query
#app initialization
app=FastAPI()
@app.get('/')
def checkHealth():
    return {"message":"okay"}

#basic dependency 
# def greet():
#     return "Hello how are you"

# @app.get('/user')
# def getUserInfo(user=Depends(greet)):
#     return user


#dependencies can take request data  
# def get_user(user_id:int):
#     return {"userId":user_id}
# @app.get('/user/{userId}')
# def getUserInfo(user=Depends(get_user)):
#     return user


# real time example 

#a.for token extraction
# def get_api_key(token:str=Header()):
#     return token
# @app.get('/user')
# def userTokenInfo(token=Depends(get_api_key)):
#     return token

#b.for authorization 
# def requrie_admin():
#     userInfo={
#         "username":"utsav",
#         "role":"admin"
#     }
#     if userInfo['role'] != "admin":
#         raise HTTPException(status_code=403,detail="Admin access require")
#     return userInfo
# @app.get('/user')
# def deleteInfo(user=Depends(requrie_admin)):
#     return {"message":"Deleted"}

#c.multiple dependencies are also possible

# def get_CurrentUser():
#      userInfo={
#             "username":"utsav",
#             "role":"admin"
#         }
#      return userInfo

# def requrie_admin():
#     userInfo={
#                "username":"utsav",
#                "role":"admin"
#            }
#     if userInfo['role'] != "admin":
#         raise HTTPException(status_code=403,detail="Admin access require")
#     return userInfo
# @app.get('/user')
# def deleteInfo(user=Depends(get_CurrentUser),permission=Depends(requrie_admin)):
#     print(user)
#     return {"message":"Deleted"}


##################################  Real time Dependencies  Example #####################################

def getUserInfo():
    return {
        "name":"utsav",
        "role":"user",
          "id":1
    }

#authorization
def require_admin(user=Depends(getUserInfo)):
    if user["role"] !="admin":
        raise HTTPException(status_code=403,detail="Admin Access Required")
    return user

#pagination
def pagination(limit:int=Query(ge=0,le=100),skip:int=1):
    return {"limit":limit,"skip":skip}

#endpoint 
@app.get('/user')
def getUserInfo(user=Depends(require_admin),
                pagination=Depends(pagination)):
    return {
        "message":"admin user endpoint",
         "required_by":user["name"],
         "skip":pagination["skip"],
         "limit":pagination["limit"]
    }

