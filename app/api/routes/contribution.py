from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.contribution import ContributionRead, ContributionCreate
from app.crud import crud_contribution
from fastapi import HTTPException
from app.db.session import get_db

router = APIRouter(prefix="/contributions", tags=["Contributions"])

# ----- Create contribution ----- #
@router.post("/", response_model=ContributionRead)
def create_contribution(contribution: ContributionCreate, db: Session = Depends(get_db)):
    return crud_contribution.create_contribution(db, contribution)

# ----- Update contribution ----- #
@router.put("/{contribution_id}", response_model=ContributionRead)
def update_contribution(contribution_id: int, contribution: ContributionCreate, db: Session = Depends(get_db)):
    db_contribution = crud_contribution.update_contribution(db, contribution_id, contribution)
    if db_contribution is None:
        raise HTTPException(status_code=404, detail="Contribution not found")
    return db_contribution

# ----- Delete contribution ----- #
@router.delete("/{contribution_id}", response_model=dict)
def delete_contribution(contribution_id: int, db: Session = Depends(get_db)):
    success = crud_contribution.delete_contribution(db, contribution_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contribution not found")
    return {"ok": True}

# ----- Read contributions ----- #
@router.get("/", response_model=list[ContributionRead])
def read_contributions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_contribution.get_contributions(db, skip=skip, limit=limit)

@router.get("/{contribution_id}", response_model=ContributionRead)
def read_contribution(contribution_id: int, db: Session = Depends(get_db)):
    db_contribution = crud_contribution.get_contribution(db, contribution_id)
    if db_contribution is None:
        raise HTTPException(status_code=404, detail="Contribution not found")
    return db_contribution

# ----- Filter contributions ----- #
@router.get("/filter/member/{member_id}", response_model=list[ContributionRead])
def filter_contributions_by_member(member_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_contribution.get_contributions_by_member(db, member_id, skip=skip, limit=limit)

@router.get("/filter/state/{state}", response_model=list[ContributionRead])
def filter_contributions_by_state(state: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_contribution.get_contributions_by_state(db, state, skip=skip, limit=limit)