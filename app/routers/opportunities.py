from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.opportunity import OpportunityCreate, OpportunityUpdate, OpportunityResponse
from app.models.opportunity import Opportunity
from app.models.user import User
from app.auth import get_current_user

router = APIRouter(prefix="/opportunities", tags=["Opportunities"])

@router.post("/", response_model=OpportunityResponse, status_code=status.HTTP_201_CREATED)
def create_opportunity(
    opportunity_data: OpportunityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    opportunity = Opportunity(**opportunity_data.model_dump())
    db.add(opportunity)
    db.commit()
    db.refresh(opportunity)
    return opportunity

@router.get("/", response_model=List[OpportunityResponse])
def get_opportunities(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    opportunities = db.query(Opportunity).offset(skip).limit(limit).all()
    return opportunities

@router.get("/{opportunity_id}", response_model=OpportunityResponse)
def get_opportunity(
    opportunity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    opportunity = db.query(Opportunity).filter(Opportunity.opportunity_id == opportunity_id).first()
    if not opportunity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity not found"
        )
    return opportunity

@router.put("/{opportunity_id}", response_model=OpportunityResponse)
def update_opportunity(
    opportunity_id: int,
    opportunity_data: OpportunityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    opportunity = db.query(Opportunity).filter(Opportunity.opportunity_id == opportunity_id).first()
    if not opportunity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity not found"
        )
    
    update_data = opportunity_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(opportunity, field, value)
    
    db.commit()
    db.refresh(opportunity)
    return opportunity

@router.delete("/{opportunity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_opportunity(
    opportunity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    opportunity = db.query(Opportunity).filter(Opportunity.opportunity_id == opportunity_id).first()
    if not opportunity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity not found"
        )
    
    db.delete(opportunity)
    db.commit()
    return None
