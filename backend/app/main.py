from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from decimal import Decimal
from typing import List
from tenacity import retry, stop_after_attempt, wait_fixed

import models, database, crud

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@retry(stop=stop_after_attempt(10), wait=wait_fixed(2))
def init_db():
    models.Base.metadata.create_all(bind=database.engine)

init_db()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field("", max_length=255)
    price: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    stock: int = Field(..., ge=0)
    is_fragile: bool = False 

class Product(ProductCreate):
    id: int
    class Config:
        orm_mode = True

@app.get("/products", response_model=List[Product])
def list_products(db: Session = Depends(get_db)):
    return crud.get_products(db)

@app.post("/products", response_model=Product)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

class SaleCreate(BaseModel):
    product_id: int
    units: int

class ProductSalesSummary(BaseModel):
    id: int
    name: str
    total_units_sold: int
    class Config:
        orm_mode = True

@app.post("/sales")
def sell_product(sale: SaleCreate, db: Session = Depends(get_db)):
    try:
        return crud.register_sale(db, sale.product_id, sale.units)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sales/summary", response_model=List[ProductSalesSummary])
def sales_summary(db: Session = Depends(get_db)):
    return crud.get_sales_summary(db)

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).get(product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
