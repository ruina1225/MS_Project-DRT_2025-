

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import jwt
from models import User
from auth import create_access_token

app = FastAPI()

SECRET_KEY = "secret_key"

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/api/login")
def login(req: LoginRequest):
    if req.username == "admin" and req.password == "1234":
        token = jwt.encode({"sub": req.username}, SECRET_KEY, algorithm="HS256")
        return {"token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
@app.post("/login")
def login(username: str, password: str):
    user = get_user_by_username(username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.username})
    return {"token": token}