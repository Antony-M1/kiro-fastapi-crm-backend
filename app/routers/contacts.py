from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.contact import ContactCreate, ContactUpdate, ContactResponse
from app.models.contact import Contact
from app.models.user import User
from app.auth import get_current_user

router = APIRouter(prefix="/contacts", tags=["Contacts"])

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(
    contact_data: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contact = Contact(**contact_data.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

@router.get("/", response_model=List[ContactResponse])
def get_contacts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contacts = db.query(Contact).offset(skip).limit(limit).all()
    return contacts

@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contact = db.query(Contact).filter(Contact.contact_id == contact_id).first()
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    return contact

@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(
    contact_id: int,
    contact_data: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contact = db.query(Contact).filter(Contact.contact_id == contact_id).first()
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    update_data = contact_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(contact, field, value)
    
    db.commit()
    db.refresh(contact)
    return contact

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contact = db.query(Contact).filter(Contact.contact_id == contact_id).first()
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    db.delete(contact)
    db.commit()
    return None
