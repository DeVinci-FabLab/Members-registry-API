from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.crud.crud_promotion import (
    create_promotion_from_descriptor,
    get_promotions,
    get_promotion,
)
from app.db.session import get_db
from app.schemas.promotion import PromotionRead

router = APIRouter(prefix="/promotions", tags=["Promotions"])


class PromotionParseIn(BaseModel):
    descriptor: str


@router.post("/parse", response_model=PromotionRead)
def create_promotion_parse(payload: PromotionParseIn, db: Session = Depends(get_db)):
    try:
        promo = create_promotion_from_descriptor(db, payload.descriptor)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return promo


@router.get("/{promotion_id}", response_model=PromotionRead)
def read_promotion(promotion_id: int, db: Session = Depends(get_db)):
    p = get_promotion(db, promotion_id)
    if not p:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return p


@router.get("/", response_model=list[PromotionRead])
def list_promotions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_promotions(db, skip=skip, limit=limit)
