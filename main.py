from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from database.mongodb import MongoDBController
from base_object import User, UpdateUser
from config import config_object

app = FastAPI()

@app.get('/')
def check_health():
    print('did good')
    return "did good"

@app.post("/users", response_model=dict)
def create_user(user: User):
    with MongoDBController() as db:
        user_data = user.model_dump()
        result = db[config_object.DB_NAME].insert_one(user_data)
        return JSONResponse(content={"user_id": str(result.inserted_id)})


@app.get("/users", response_model=List[dict])
def get_all_users():
    with MongoDBController() as db:
        users = list(db[config_object.DB_NAME].find({}, {"_id": 0}))
        return JSONResponse(content=users)


@app.get("/users/{id}", response_model=dict)
def get_user(id: str):
    with MongoDBController() as db:
        user = db[config_object.DB_NAME].find_one({"id": id}, {"_id": 0})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return JSONResponse(content=user)


@app.put("/users/{id}", response_model=dict)
def update_user(id: str, update_data: UpdateUser):
    with MongoDBController() as db:
        update_query = {k: v for k, v in update_data.model_dump().items() if v is not None}
        result = db[config_object.DB_NAME].update_one({"id": id}, {"$set": update_query})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return JSONResponse(content={"updated_count": result.modified_count})


@app.delete("/users/{id}", response_model=dict)
def delete_user(id: str):
    with MongoDBController() as db:
        result = db[config_object.DB_NAME].delete_one({"id": id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return JSONResponse(content={"deleted_count": result.deleted_count})

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=config_object.HOST_NAME,
        port=config_object.PORT,
        proxy_headers=True
    )