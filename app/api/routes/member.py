from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.member import MemberRead, MemberCreate
from app.crud.crud_member import get_member, get_members, create_member, update_member, delete_member
from app.exceptions.http_exceptions import UserNotFoundException, EmailAlreadyExistsException
from app.db.session import get_db

router = APIRouter(prefix="/members", tags=["Members"])

@router.get("/", response_model=list[MemberRead])
def read_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_members(db, skip=skip, limit=limit)

@router.get("/{member_id}", response_model=MemberRead)
def read_member(member_id: int, db: Session = Depends(get_db)):
    db_member = get_member(db, member_id)
    if db_member is None:
        raise UserNotFoundException()
    return db_member

@router.post("/", response_model=MemberRead)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    return create_member(db, member)

@router.put("/{member_id}", response_model=MemberRead)
def update_member(member_id: int, member: MemberCreate, db: Session = Depends(get_db)):
    updated = update_member(db, member_id, member)
    if updated is None:
        raise UserNotFoundException()
    return updated

@router.delete("/{member_id}", response_model=dict)
def delete_member(member_id: int, db: Session = Depends(get_db)):
    success = delete_member(db, member_id)
    if not success:
        raise UserNotFoundException()
    return {"ok": True}
