from sqlalchemy.orm import Session
from sqlalchemy import func
import models

def get_products(db: Session):
    return db.query(models.Product).all()

def create_product(db: Session, product_data):
    product = models.Product(**product_data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def register_sale(db: Session, product_id: int, units: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product or product.stock < units:
        raise ValueError("Insufficient stock or product not found")

    product.stock -= units
    sale = models.Sale(product_id=product_id, units=units)
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale

def get_sales_summary(db: Session):
    result = (
        db.query(models.Product.id, models.Product.name, func.sum(models.Sale.units).label("total_units_sold"))
        .join(models.Sale)
        .group_by(models.Product.id)
        .all()
    )
    return result
