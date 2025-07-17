from sqlalchemy.orm import Session
from app.models.member import Member
from app.schemas.member import MemberCreate

def get_member(db: Session, member_id: int) -> Member | None:
    return db.query(Member).filter(Member.id == member_id).first()

def get_members(db: Session, skip: int = 0, limit: int = 100) -> list[Member]:
    return db.query(Member).offset(skip).limit(limit).all()

def create_member(db: Session, member: MemberCreate) -> Member:
    db_member = Member(firstame=member.first_name,
                       last_name=member.last_name,
                       present=member.present,)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def update_member(db: Session, member_id: int, member: MemberCreate) -> Member | None:
    db_member = get_member(db, member_id)
    if db_member is None:
        return None
    db_member.first_name = member.first_name
    db_member.last_name = member.last_name
    db_member.present = member.present
    db.commit()
    db.refresh(db_member)
    return db_member

def delete_member(db: Session, member_id: int) -> bool:
    db_member = get_member(db, member_id)
    if db_member is None:
        return False
    db.delete(db_member)
    db.commit()
    return True
