from sqlalchemy.orm import Session
from app.models.member import Member
from app.models.major import Major
from app.models.promotion import Promotion
from app.models.status import Status
from app.schemas.member import MemberCreate

def get_member(db: Session, member_id: int) -> Member | None:
    return db.query(Member).filter(Member.id == member_id).first()

def get_members(db: Session, skip: int = 0, limit: int = 100) -> list[Member]:
    return db.query(Member).offset(skip).limit(limit).all()

def create_member(db: Session, member: MemberCreate) -> Member:
    db_member = Member(
        first_name=member.first_name,
        last_name=member.last_name,
        email=member.email,  
        personal_email=member.personal_email,
        present=member.present,
        arrival=member.arrival,
        departure=member.departure,
        phone=member.phone,
        discord=member.discord,
        notes=member.notes,
        srg=member.srg,
        warning=member.warning,
        created_by=member.created_by,
        created_at=member.created_at,
        modified_by=member.modified_by,
        modified_at=member.modified_at,
        convs=member.convs,
        portal=member.portal,
        promotion_id=member.promotion_id,
    )
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


def get_members_by_major(db: Session, major_id: int):
    return (
        db.query(Member)
        .join(Promotion, Member.promotion_id == Promotion.id)
        .join(Major, Promotion.major_id == Major.id)
        .filter(Major.id == major_id)
        .all()
    )

def get_members_by_status(db: Session, status_id: int) -> list[Member]:
    return db.query(Member).join(Member.statuses).filter(Status.id == status_id).all()