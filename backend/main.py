from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI(title="Week2 Webdesign")

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

items: list[dict[str, Any]] = [{"id": 1, "name": "Laptop", "price": 999.99}]
next_item_id = 2


class ItemCreate(BaseModel):
    name: str
    price: float | None = None


class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None


class ItemPublic(BaseModel):
    id: int
    name: str
    price: float | None = None


class ItemListResponse(BaseModel):
    items: list[ItemPublic]
    total: int
    skip: int
    limit: int


class HousePriceRequest(BaseModel):
    area_sqm: float = Field(gt=0)
    bedrooms: int = Field(ge=0)
    distance_to_center_km: float


class HousePricePrediction(BaseModel):
    predicted_price: float
    currency: str = "VND"


def _item_name_exists(name: str, exclude_id: int | None = None) -> bool:
    normalized = name.strip().lower()
    for item in items:
        if exclude_id is not None and item["id"] == exclude_id:
            continue
        if str(item["name"]).strip().lower() == normalized:
            return True
    return False


@app.get("/api/health")
def health_check():
    return {"status": "ok", "items_count": len(items)}


@app.get("/api/message")
def get_message():
    return {"message": "Hello from backend!", "source": "FastAPI"}


@app.get("/api/items", response_model=ItemListResponse)
def list_items(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    min_price: float | None = Query(default=None),
    max_price: float | None = Query(default=None),
    q: str | None = Query(default=None, min_length=2),
    sort_by: str = Query(default="id", pattern="^(id|name|price)$"),
    order: str = Query(default="asc", pattern="^(asc|desc)$"),
):
    filtered = list(items)

    if min_price is not None:
        filtered = [item for item in filtered if (item.get("price") is not None and item["price"] >= min_price)]
    if max_price is not None:
        filtered = [item for item in filtered if (item.get("price") is not None and item["price"] <= max_price)]
    if q is not None:
        q_lower = q.lower()
        filtered = [item for item in filtered if q_lower in str(item["name"]).lower()]

    if sort_by == "name":
        filtered = sorted(filtered, key=lambda item: str(item.get("name", "")).lower(), reverse=(order == "desc"))
    elif sort_by == "price":
        filtered = sorted(
            filtered,
            key=lambda item: (item.get("price") is None, item.get("price") if item.get("price") is not None else 0.0),
            reverse=(order == "desc"),
        )
    else:
        filtered = sorted(filtered, key=lambda item: item.get("id", 0), reverse=(order == "desc"))

    total = len(filtered)
    paged_items = filtered[skip : skip + limit]

    return ItemListResponse(items=paged_items, total=total, skip=skip, limit=limit)


@app.get("/api/items/{item_id}", response_model=ItemPublic)
def get_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/api/items", status_code=201, response_model=ItemPublic)
def create_item(item: ItemCreate):
    global next_item_id

    if _item_name_exists(item.name):
        raise HTTPException(status_code=409, detail="Item with this name already exists")

    new_item = {"id": next_item_id, "name": item.name, "price": item.price}
    items.append(new_item)
    next_item_id += 1
    return new_item


@app.put("/api/items/{item_id}", response_model=ItemPublic)
def update_item(item_id: int, item: ItemCreate):
    for index, existing_item in enumerate(items):
        if existing_item["id"] == item_id:
            if item.name.lower() != existing_item["name"].lower() and _item_name_exists(item.name, exclude_id=item_id):
                raise HTTPException(status_code=409, detail="Item with this name already exists")
            items[index]["name"] = item.name
            items[index]["price"] = item.price
            return items[index]
    raise HTTPException(status_code=404, detail="Item not found")


@app.patch("/api/items/{item_id}", response_model=ItemPublic)
def patch_item(item_id: int, item: ItemUpdate):
    for index, existing_item in enumerate(items):
        if existing_item["id"] == item_id:
            updates = item.model_dump(exclude_unset=True)
            if not updates:
                return existing_item

            new_name = updates.get("name")
            if new_name is not None and new_name.lower() != existing_item["name"].lower():
                if _item_name_exists(new_name, exclude_id=item_id):
                    raise HTTPException(status_code=409, detail="Item with this name already exists")

            for field, value in updates.items():
                if value is not None:
                    items[index][field] = value
            return items[index]
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/api/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    for index, existing_item in enumerate(items):
        if existing_item["id"] == item_id:
            del items[index]
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/predict/house-price", response_model=HousePricePrediction)
def predict_house_price(payload: HousePriceRequest):
    predicted_price = (
        payload.area_sqm * 15_000_000
        - payload.distance_to_center_km * 5_000_000
        + payload.bedrooms * 20_000_000
    )
    return HousePricePrediction(predicted_price=predicted_price)


app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
