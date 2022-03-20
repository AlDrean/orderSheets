from fastapi.testclient import TestClient

from sql_ordersheet.main import app
from sql_ordersheet import schemas

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_insert_item():
    response = client.post(
        "/items/",
        json={
            "name": "cavalo",
            "hashId": "dsadsaddd",
            "price": 1
        }
    )
    assert response.status_code == 200
    assert response.json() == {
                              "name": "cavalo",
                              "hashId": "5368811147044902053",
                              "price": 1,
                              "id": 2,
                              "active": True
                            }
    response = client.get("/items/")
    assert response.json() == {
        "name": "cavalo",
        "hashId": "5368811147044902053",
        "price": 1,
        "id": 2,
        "active": True
    }


    assert response.status_code == 200


