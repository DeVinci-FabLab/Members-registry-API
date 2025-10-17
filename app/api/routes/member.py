from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.member import MemberRead, MemberCreate
from app.crud import crud_member
from app.exceptions.http_exceptions import UserNotFoundException, EmailAlreadyExistsException
from app.db.session import get_db

router = APIRouter(prefix="/members", tags=["Members"])

# ----- Create member ----- #
@router.post("/", response_model=MemberRead)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    return crud_member.create_member(db, member)

# ----- Update member ----- #
@router.put("/{member_id}", response_model=MemberRead)
def update_member(member_id: int, member: MemberCreate, db: Session = Depends(get_db)):
    db_member = crud_member.update_member(db, member_id, member)
    if db_member is None:
        raise UserNotFoundException()
    return db_member

# ----- Delete member ----- #
@router.delete("/{member_id}", response_model=dict)
def delete_member(member_id: int, db: Session = Depends(get_db)):
    success = crud_member.delete_member(db, member_id)
    if not success:
        raise UserNotFoundException()
    return {"ok": True}

# ----- Read members ----- #
@router.get("/", response_model=list[MemberRead])
def read_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_member.get_members(db, skip=skip, limit=limit)

@router.get("/{member_id}", response_model=MemberRead)
def read_member(member_id: int, db: Session = Depends(get_db)):
    db_member = crud_member.get_member(db, member_id)
    if db_member is None:
        raise UserNotFoundException()
    return db_member

# ----- Filter members ----- #
@router.get("/filter/major/{major_id}", response_model=list[MemberRead])
def filter_members_by_major(major_id: int, db: Session = Depends(get_db)):
    return crud_member.get_members_by_major(db, major_id)

@router.get("/filter/status/{status_id}", response_model=list[MemberRead])
def filter_members_by_status(status_id: int, db: Session = Depends(get_db)):
    return crud_member.get_members_by_status(db, status_id)