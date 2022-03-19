from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from urllib import response

from models import (
    Life_Pydantic,
    LifeIn_Pydantic,
    LifeInput,
    LifeInput_Pydantic
)

# créer le post create 

class Message(BaseModel):
    message: str


app = FastAPI()

@app.post("/life", response_model=LifeInput_Pydantic)
async def create(life: LifeInput_Pydantic):
    print("start")
    obj = await LifeInput.create(**life.dict(), exclude_unset=True)
    print("obj")
    return await LifeInput_Pydantic.from_tortoise_orm(obj)

register_tortoise(
    app,
    db_url='sqlite://store.db',
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True
)

# ce qui es en dessous va nous permettre de recupérer le post create.
# qui est au dessous. ( rest get)

@app.get('/life/{id}', response_model=LifeInput_Pydantic, responses={404: {'models': HTTPNotFoundError}})
async def get_one(id: int):
    return await LifeInput_Pydantic.from_queryset_single(LifeInput.get(id=id))

# Faire un update, pour en faire un on doit a avoir l'id.
@app.put("/life/{id}", response_model=Life_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_life(id: int, life: LifeIn_Pydantic):
    await LifeInput.filter(id=id).update(**life.dict(exclude_unset=True))
    return await Life_Pydantic.from_queryset_single(LifeInput.get(id=id))


# On a fait le delete qui sert a supprimer un post dans notre base de donné
# pour ça on a besoin de l'ID
@app.delete('/life/{id}', response_model = Message, responses={404: {'model': HTTPNotFoundError}})
async def delete_life(id: int):
    delete_obj = await LifeInput.filter(id=id).delete()
    if not delete_obj:
        raise HTTPException(status_code=404, detail= 'this life is not found')
    return Message(message = 'Successfuly deleted')            