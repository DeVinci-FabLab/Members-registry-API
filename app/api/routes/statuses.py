from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.status import MemberStatus, StatusCreate, StatusRead
from app.crud import crud_statuses
from app.db.session import get_db
from app.exceptions.http_exceptions import StatusNotFoundException, UserNotFoundException

router = APIRouter(prefix="/statuses", tags=["Statuses"])

@router.post("/", response_model=StatusRead)
def create_status(status: StatusCreate, db: Session = Depends(get_db)):
    return crud_statuses.create_status(db, status)

@router.get("/", response_model=list[StatusRead])
def read_statuses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_statuses.get_statuses(db, skip=skip, limit=limit)

@router.get("/{status_id}", response_model=StatusRead)
def read_status(status_id: int, db: Session = Depends(get_db)):
    db_status = crud_statuses.get_status(db, status_id)
    if db_status is None:
        raise StatusNotFoundException
    return db_status

@router.delete("/{status_id}", response_model=dict)
def delete_status(status_id: int, db: Session = Depends(get_db)):
    success = crud_statuses.delete_status(db, status_id)
    if not success:
        raise StatusNotFoundException()
    return {"ok": True}

@router.post("/assign", response_model=dict)
def assign_status_to_member(payload: MemberStatus, db: Session = Depends(get_db)):
    success = crud_statuses.asign_status_to_member(db, payload.member_id, payload.status_id)
    if not success:
        raise UserNotFoundException()
    return {"ok": True}

@router.post("/remove", response_model=dict)
def remove_status_from_member(payload: MemberStatus, db: Session = Depends(get_db)):
    success = crud_statuses.remove_status_from_member(db, payload.member_id, payload.status_id)
    if not success:
        raise UserNotFoundException()
    return {"ok": True}

