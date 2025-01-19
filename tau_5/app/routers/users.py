from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

users = [
    {"id": 1, "name": "Jan Kowalski", "email": "jan@kowalski.pl"},
    {"id": 2, "name": "Anna Nowak", "email": "anna@nowak.pl"},
]

class User(BaseModel):
    name: str
    email: str

@router.get("/users")
def get_users():
    return users

@router.get("/users/{id}")
def get_user(id: int):
    user = next((user for user in users if user["id"] == id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users", status_code=201)
def create_user(user: User):
    new_user = {"id": len(users) + 1, "name": user.name, "email": user.email}
    users.append(new_user)
    return new_user

@router.put("/users/{id}")
def update_user(id: int, user: User):
    existing_user = next((u for u in users if u["id"] == id), None)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    existing_user.update({"name": user.name, "email": user.email})
    return existing_user

@router.delete("/users/{id}", status_code=204)
def delete_user(id: int):
    global users
    users = [user for user in users if user["id"] != id]
    return {"message": "User deleted"}
