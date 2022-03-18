from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from . import models, schemas, main


def get_item_id(db: Session, item_id: int):
    return db.query(models.Items).filter(models.Items.id == item_id).first()


def get_item(db: Session, item_name: str):
    return db.query(models.Items).filter(models.Items.name == item_name).first()


def get_items(db: Session, skip: int = 0, limit=100):
    return db.query(models.Items).offset(skip).limit(limit).all()


def get_orderSheet_(db: Session, hash_order_id: str):
    return db.query(models.OrderSheet).filter(models.OrderSheet.hash_order_id == hash_order_id).all()


def update_item(db: Session, item: schemas.Item):
    db_item = db.query(models.Items).filter(models.Items.id == item.id).update(
        {"name": item.name,
         "price": item.price,
         "active": item.active
         }
    )

    db.commit()
    db.flush()

    return item


#def update_items(db: Session, items: List[schemas.Item]):
#    for item in items:
#        db.query(models.Items).filter(models.Items.id == item.id).update(
#            {"name": item.name,
#             "price": item.price,
#             "active": item.active
#             }
#        )


# def get_orderSheet(db: Session, hash_: str):
#    return db.query(models.OrderSheet).filter(models.OrderSheet.hash_order_id == hash_).all()


def get_orderSheets(db: Session, skip: int = 0, limit=100):
    return db.query(models.OrderSheet).offset(skip).limit(limit).all()


def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Items(name=item.name, price=item.price, hashId=hash(item.name))
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_orderSheet(db: Session, osheet: schemas.OrderSheetCreate, hash_=None):
    db_return = []

    if hash_ == "":
        hash_ = (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    for item in osheet.items:
        db_osheet = models.OrderSheet(hash_order_id=f"{main.LOCAL_HASH} {hash_}", item=item)
        db.add(db_osheet)
        db.commit()
        db.refresh(db_osheet)
        db_return.append(db_osheet)
    return db_return
