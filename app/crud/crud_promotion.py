from __future__ import annotations
from typing import Optional, Tuple
import re
from datetime import date

from sqlalchemy.orm import Session, joinedload

from app.models.promotion import Promotion
from app.models.school import School
from app.models.level import Level
from app.models.major import Major

def get_promotion(db: Session, promotion_id: int) -> Optional[Promotion]:
    return db.query(Promotion).options(
        joinedload(Promotion.level),
        joinedload(Promotion.school),
        joinedload(Promotion.major),
    ).filter(Promotion.id == promotion_id).first()

def get_promotions(db: Session, skip: int = 0, limit: int = 100) -> list[Promotion]:
    return db.query(Promotion).options(
        joinedload(Promotion.level),
        joinedload(Promotion.school),
        joinedload(Promotion.major),
    ).offset(skip).limit(limit).all()

def get_majors(db: Session, skip: int = 0, limit: int = 100) -> list[Major]:
    return db.query(Major).offset(skip).limit(limit).all()

def get_levels(db: Session, skip: int = 0, limit: int = 100) -> list[Level]:
    return db.query(Level).offset(skip).limit(limit).all()

def get_schools(db: Session, skip: int = 0, limit: int = 100) -> list[School]:
    return db.query(School).offset(skip).limit(limit).all()

def _get_or_create_school(db: Session, name: str) -> School:
    name = name.strip()
    school = db.query(School).filter(School.name.ilike(name)).first()
    if school:
        return school
    school = School(name=name)
    db.add(school)
    db.flush()
    return school

def _get_or_create_level(db: Session, level_name: str) -> Level:
    # Accept "A4", "ANNEE 4", "4"
    ln = level_name.strip().upper()
    m = re.search(r'\bA\s*(\d)\b', ln) or re.search(r'\bANNEE\s*(\d)\b', ln) or re.search(r'\b(\d)\b', ln)
    if m:
        name = f"A{m.group(1)}"
    else:
        name = ln
    level = db.query(Level).filter(Level.name.ilike(name)).first()
    if level:
        return level
    level = Level(name=name, order=int(m.group(1)) if m else None)
    db.add(level)
    db.flush()
    return level

def _get_or_create_major(db: Session, name: str, school_id: int, level_id: Optional[int]) -> Major:
    if not name:
        return None
    name_clean = name.strip().upper()

    code_level = f"{name_clean}_{level_id}"

    # Vérifier si ça existe déjà
    q = db.query(Major).filter(
        Major.code == code_level,
        Major.school_id == school_id,
        Major.level_id == level_id
    )
    major = q.first()
    if major:
        return major

    # Créer si absent
    major = Major(
        name=name_clean,
        code=code_level,
        school_id=school_id,
        level_id=level_id
    )
    db.add(major)
    db.flush()
    return major

def parse_descriptor(descriptor: str) -> Tuple[Optional[str], Optional[str], Optional[str], bool, Optional[int]]:
    """
    Examples:
      "Étudiants ESILV A4 CREATECH_E 2024"
      "Étudiants ESILV A4 OCC 2025"
      "Étudiants IIM A4 ALT DA 2024"

    Returns:
      (school_name, level_token, major_name, is_apprentice, year)
    """
    text = descriptor.strip()
    # Remove prefix like "Étudiants" or similar
    text = re.sub(r'^(Étudiants|Etudiants|Etudiant|Étudiant)\s+', '', text, flags=re.IGNORECASE)

    # Extract year (4 digits at the end)
    year_match = re.search(r'(\d{4})$', text)
    year = int(year_match.group(1)) if year_match else None
    if year:
        text = text[:year_match.start()].strip()

    # Extract school (assume first token)
    tokens = text.split()
    if not tokens:
        return None, None, None, False, year

    school = tokens[0].upper()
    remaining = tokens[1:]

    # Extract level (A1, A2, A3, A4, A5, ANNEE X)
    level_token = None
    for i, t in enumerate(remaining):
        if re.match(r'^A\d$', t.upper()) or re.match(r'^ANNEE\s*\d$', t.upper()):
            level_token = t.upper().replace("ANNEE", "A").strip()
            remaining = remaining[i + 1 :]
            break

    # Detect alternance
    is_appr = any("ALT" in t.upper() or "ALTERNANCE" in t.upper() for t in remaining)

    # Remove ALT / ALTERNANCE tokens from major
    major_tokens = [t for t in remaining if not re.match(r'ALT(ERNANCE)?', t, re.IGNORECASE)]
    major = " ".join(major_tokens).strip() if major_tokens else None

    return school, level_token, major, is_appr, year


def create_promotion_from_descriptor(db: Session, descriptor: str) -> Promotion:
    school_name, level_token, major_name, is_appr, year = parse_descriptor(descriptor)
    if not school_name:
        raise ValueError(f"Cannot determine school from descriptor: {descriptor}")

    promotion_year = year or date.today().year

    # ensure entities exist
    school = _get_or_create_school(db, school_name)
    level = _get_or_create_level(db, level_token or "A1")
    major = _get_or_create_major(db, major_name, school.id, level.id) if major_name else None

    # Check existing
    existing = db.query(Promotion).filter(
        Promotion.school_id == school.id,
        Promotion.level_id == level.id,
        Promotion.year == promotion_year,
        Promotion.major_id == (major.id if major else None),
        Promotion.is_apprentice == bool(is_appr)
    ).first()

    if existing:
        return existing

    promo = Promotion(
        year=promotion_year,
        level_id=level.id,
        school_id=school.id,
        major_id=(major.id if major else None),
        is_apprentice=is_appr,
    )
    db.add(promo)
    db.commit()
    db.refresh(promo)
    return promo

def create_promotion(db: Session, year: int, level_id: int, school_id: int, major_id: Optional[int], is_apprentice: bool) -> Promotion:
    promo = Promotion(
        year=year,
        level_id=level_id,
        school_id=school_id,
        major_id=major_id,
        is_apprentice=is_apprentice,
    )
    db.add(promo)
    db.commit()
    db.refresh(promo)
    return promo

def delete_promotion(db: Session, promotion_id: int) -> bool:
    promo = get_promotion(db, promotion_id)
    if promo is None:
        return False
    db.delete(promo)
    db.commit()
    return True

def update_promotion(db: Session, promotion_id: int, year: Optional[int] = None, level_id: Optional[int] = None,
                     school_id: Optional[int] = None, major_id: Optional[int] = None,
                     is_apprentice: Optional[bool] = None) -> Optional[Promotion]:
    promo = get_promotion(db, promotion_id)
    if promo is None:
        return None
    if year is not None:
        promo.year = year
    if level_id is not None:
        promo.level_id = level_id
    if school_id is not None:
        promo.school_id = school_id
    if major_id is not None:
        promo.major_id = major_id
    if is_apprentice is not None:
        promo.is_apprentice = is_apprentice
    db.commit()
    db.refresh(promo)
    return promo

def delete_promotion(db: Session, promotion_id: int) -> bool:
    promo = get_promotion(db, promotion_id)
    if promo is None:
        return False
    db.delete(promo)
    db.commit()
    return True

def get_promotions_by_major(db: Session, major_id: int) -> list[Promotion]:
    return db.query(Promotion).filter(Promotion.major_id == major_id).all()