from sqlalchemy.orm import Session
from app.models.contribution import Contribution
from app.schemas.contribution import ContributionCreate

def create_contribution(db: Session, contribution: ContributionCreate) -> Contribution:
    db_contribution = Contribution(
        member_id=contribution.member_id,
        state=contribution.state,
        payment_date=contribution.payment_date,
        amount=contribution.amount,
    )
    db.add(db_contribution)
    db.commit()
    db.refresh(db_contribution)
    return db_contribution

def get_contribution(db: Session, contribution_id: int) -> Contribution | None:
    return db.query(Contribution).filter(Contribution.id == contribution_id).first()

def get_contributions(db: Session, skip: int = 0, limit: int = 100) -> list[Contribution]:
    return db.query(Contribution).offset(skip).limit(limit).all()

def update_contribution(db: Session, contribution_id: int, contribution: ContributionCreate) -> Contribution | None:
    db_contribution = get_contribution(db, contribution_id)
    if db_contribution is None:
        return None
    for key, value in contribution.model_dump(exclude_unset=True).items():
        setattr(db_contribution, key, value)
    db.commit()
    db.refresh(db_contribution)
    return db_contribution

def delete_contribution(db: Session, contribution_id: int) -> bool:
    db_contribution = get_contribution(db, contribution_id)
    if db_contribution is None:
        return False
    db.delete(db_contribution)
    db.commit()
    return True

def get_contributions_by_member(db: Session, member_id: int, skip: int = 0, limit: int = 100) -> list[Contribution]:
    return db.query(Contribution).filter(Contribution.member_id == member_id).offset(skip).limit(limit).all()

def get_contributions_by_state(db: Session, state: str, skip: int = 0, limit: int = 100) -> list[Contribution]:
    return db.query(Contribution).filter(Contribution.state == state).offset(skip).limit(limit).all()

