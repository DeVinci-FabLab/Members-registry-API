from sqlalchemy.orm import Session
from app.models.status import Status
from app.models.member import Member
from app.schemas.status import StatusCreate
from typing import List, Optional


# ✅ Récupérer un seul statut par ID
def get_status(db: Session, status_id: int) -> Optional[Status]:
    return db.query(Status).filter(Status.id == status_id).first()


# ✅ Récupérer plusieurs statuts (liste)
def get_statuses(db: Session, skip: int = 0, limit: int = 100) -> List[Status]:
    return db.query(Status).offset(skip).limit(limit).all()


# ✅ Créer un statut
def create_status(db: Session, status : StatusCreate) -> Status:
    db_status = Status(name=status.name)
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status


# ✅ Supprimer un statut
def delete_status(db: Session, status_id: int) -> bool:
    db_status = get_status(db, status_id) 
    if db_status is None:
        return False
    db.delete(db_status)
    db.commit()
    return True


# ✅ Assigner un statut à un membre
def asign_status_to_member(db: Session, member_id: int, status_id: int) -> bool:
    db_status = get_status(db, status_id)
    if db_status is None:
        return False

    db_member = db.query(Member).filter(Member.id == member_id).first()
    if db_member is None:
        return False

    # Éviter les doublons
    if db_status not in db_member.statuses:
        db_member.statuses.append(db_status)
        db.commit()
        db.refresh(db_member)
    return True


# ✅ Retirer un statut d’un membre
def remove_status_from_member(db: Session, member_id: int, status_id: int) -> bool:
    db_status = get_status(db, status_id)
    if db_status is None:
        return False

    db_member = db.query(Member).filter(Member.id == member_id).first()
    if db_member is None:
        return False

    if db_status in db_member.statuses:
        db_member.statuses.remove(db_status)
        db.commit()
        db.refresh(db_member)
        return True
    return False
