# @TODO: atualizar todos os textos para maiuscula em prol de conscistência e facilitar o filtro
# @TODO: rever utilizar hash() para fazer os hashs, não tão sendo conscistentes

# @TODO: revisar os entry e os fluxos
# @TODO: como pensar sobre a responsabilidade do consumo ser do restaurante?
# @TODO: Automatização de testes para  a API

# @TODO:Fazer migração o para a base de dados
# @TODO: levantar em container


# @TODO: Fazer um  app consumidor python/cotlin para automatizar a população do banco?
# @TODO: Fazer um  app d e atk à porta da api


from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud

from .database import SessionLocal, engine

LOCAL_HASH = "<nome_estabelecimento>"
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/item/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_name=item.name)
    if db_item:
        raise HTTPException(status_code=400, detail="Item already registered")
    return crud.create_item(db=db, item=item)


@app.put("/item/{item_id}", response_model=schemas.Item)
def update_item(items_id: int, item: schemas.Item, db: Session = Depends(get_db)):
    db_item = crud.get_item_id(db, item_id=items_id)
    if not db_item:
        return crud.update_item(db=db, item=item)


# @TODO: encontrar um jeito melhor que criar u ma exceção de html caso um dos itens da lista esteja repitido
@app.post("/items/", response_model=List[schemas.Item])
def create_item(items: List[schemas.ItemCreate], db: Session = Depends(get_db)):
    db_items = []

    for item in items:
        db_item = crud.get_item(db, item_name=item.name)
        # @TODO here
        if not db_item:
            db_items.append(crud.create_item(db=db, item=item))
    return db_items


@app.put("/items/", response_model=List[schemas.Item])
def update_items(items: List[schemas.Item], db: Session = Depends(get_db)):
    db_items = []
    for item in items:
        db_item = crud.get_item_id(db, item_id=item.id)
        if db_item:
            db_item = crud.update_item(db=db, item=item)
            db_items.append(db_item)
    return db_items


@app.get("/items/{item_id}", response_model=schemas.Item)
def read_items(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item_id(db, item_id=item_id)
    if db_item:
        return db_item
    raise HTTPException(status_code=400, detail="Item not found")



@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_items = crud.get_items(db, skip=skip, limit=limit)
    return db_items



@app.post("/orderSheets/", response_model=List[schemas.OrderSheet])
def read_orderSheets(order_sheet: schemas.OrderSheetCreate, db: Session = Depends(get_db)):
    db_order_sheet = crud.create_orderSheet(db, order_sheet,
                                            hash_=order_sheet.hash_order_id)

    return db_order_sheet


@app.get("/orderSheets/", response_model=List[schemas.OrderSheet])
def get_orderSheets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_orderSheets = crud.get_orderSheets(db, skip=skip, limit=limit)
    return db_orderSheets


@app.get("/orderSheets/{hash_}", response_model=List[schemas.OrderSheet])
def get_orderSheet(hash_: str, db: Session = Depends(get_db)):
    db_orderSheet = crud.get_orderSheet_(db, hash_order_id=hash_)
    if not db_orderSheet:
        raise HTTPException(status_code=400, detail="Order sheet not found")
    return db_orderSheet


@app.get("/qrcode/teste/")
def qrCodeLimitest():
    array = [i for i in range(4296)]
    return array
