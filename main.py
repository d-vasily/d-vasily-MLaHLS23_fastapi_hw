from typing import Dict, List
from enum import Enum
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel
from typing import Dict

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/', summary='Root')
def root():
    return ('string')


@app.post("/post", summary='Get Post')
def post() -> Timestamp:
    post_db.append(Timestamp(id=post_db[-1].id + 1, timestamp = 10))
    return post_db[-1]


@app.post("/dog", summary='Create Dog', response_model=Dog)
def create_dog(dog: Dog) -> Dog:
    dogs_db[max(dogs_db.keys()) + 1] = dog
    return dog


@app.get("/dog", summary='Get Dogs')
def get_dogs(kind: str = Query(pattern="terrier|bulldog|dalmatian")) -> List:
    return [{"name": dogs_db[k].name, "pk": dogs_db[k].pk, "kind": dogs_db[k].kind}\
            for k in dogs_db.keys() if dogs_db[k].kind == kind]


@app.get("/dog/{pk}", summary='Get Dog By Pk')
def get_dog_by_pk(pk: int) -> Dog:
    for k in dogs_db.keys():
        if dogs_db[k].pk == pk:
            return dogs_db[k]


@app.patch("/dog/{pk}", summary='Update Dog')
def update_dog(pk: int, dog: Dog) -> Dog:
    for k in dogs_db.keys():
        if dogs_db[k].pk == pk:
            dogs_db[k] = dog
            return dog
        
    dogs_db[max(dogs_db.keys()) + 1] = dog
    return dog
