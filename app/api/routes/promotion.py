from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.crud.crud_promotion import (
    create_promotion_from_descriptor,
    get_promotions,
    get_promotion,
    get_levels,
    get_schools,
    get_majors,
    delete_promotion,
    update_promotion,
    create_promotion,
    get_promotions_by_major,
)
from app.db.session import get_db
from app.schemas.promotion import PromotionRead, SchoolRead, LevelRead, MajorRead

router = APIRouter(prefix="/promotions", tags=["Promotions"])

class PromotionParseIn(BaseModel):
    descriptor: str

# ----- Create promotion ----- #

@router.post("/parse", response_model=PromotionRead)
def create_promotion_parse(payload: PromotionParseIn, db: Session = Depends(get_db)):
    try:
        promo = create_promotion_from_descriptor(db, payload.descriptor)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return promo

@router.post("/", response_model=PromotionRead)
def create_promotion_direct(
    year: int,
    level_id: int,
    school_id: int,
    major_id: Optional[int] = None,
    is_apprentice: bool = False,
    db: Session = Depends(get_db),
):
    promo = create_promotion(db, year, level_id, school_id, major_id, is_apprentice)
    return promo

# ----- Update promotion ----- #
@router.put("/{promotion_id}", response_model=PromotionRead)
def update_promotion_endpoint(
    promotion_id: int,
    year: Optional[int] = None,
    level_id: Optional[int] = None,
    school_id: Optional[int] = None,
    major_id: Optional[int] = None,
    is_apprentice: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    promo = update_promotion(db, promotion_id, year, level_id, school_id, major_id, is_apprentice)
    if not promo:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return promo

# ----- Delete promotion ----- #
@router.delete("/{promotion_id}", response_model=dict)
def delete_promotion_endpoint(promotion_id: int, db: Session = Depends(get_db)):
    success = delete_promotion(db, promotion_id)
    if not success:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return {"detail": "Promotion deleted successfully"}

# ----- Get lists ----- #

@router.get("/{promotion_id}", response_model=PromotionRead)
def read_promotion(promotion_id: int, db: Session = Depends(get_db)):
    p = get_promotion(db, promotion_id)
    if not p:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return p

@router.get("/", response_model=list[PromotionRead])
def list_promotions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_promotions(db, skip=skip, limit=limit)

@router.get("/majors/", response_model=list[MajorRead])
def list_majors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_majors(db, skip=skip, limit=limit)

@router.get("/schools/", response_model=list[SchoolRead])
def list_schools(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_schools(db, skip=skip, limit=limit)

@router.get("/levels/", response_model=list[LevelRead])
def list_levels(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_levels(db, skip=skip, limit=limit)

# ----- Filter promotions by major ----- #
@router.get("/filter/major/{major_id}", response_model=list[PromotionRead])
def filter_promotions_by_major(major_id: int, db: Session = Depends(get_db)):
    return get_promotions_by_major(db, major_id)