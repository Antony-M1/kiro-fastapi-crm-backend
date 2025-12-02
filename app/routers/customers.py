from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from app.models.customer import Customer
from app.models.user import User
from app.auth import get_current_user

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    customer = Customer(**customer_data.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

@router.get("/", response_model=List[CustomerResponse])
def get_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    customers = db.query(Customer).offset(skip).limit(limit).all()
    return customers

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return customer

@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    update_data = customer_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(customer, field, value)
    
    db.commit()
    db.refresh(customer)
    return customer

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    db.delete(customer)
    db.commit()
    return None
