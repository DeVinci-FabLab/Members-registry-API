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

def parse_descriptor(descriptor: str) -> Tuple[Optional[str], Optional[str], Optional[str], bool]:
    """
    Parse descriptor examples:
      "ESILV ANNEE 4 - IRO"
      "IIM - ANNEE 5 - ALTERNANCE - DIRECTION ARTISTIQUE"
      "ESILV ANNEE 3"
    Returns (school_name, level_token, major_name, is_apprentice)
    """
    parts = [p.strip() for p in re.split(r'[-/]', descriptor) if p.strip()]
    school = None
    level_token = None
    major = None
    is_appr = False

    # Flatten tokens and search for keywords
    tokens = []
    for p in parts:
        tokens.extend([t.strip() for t in re.split(r'\s{2,}|\s-\s', p) if t.strip()])

    # heuristic: school is first token until we see "ANNEE" or "A\d"
    combined = " ".join(parts)
    # find level
    m = re.search(r'\bANNEE\s*(\d)\b', combined, flags=re.IGNORECASE)
    if not m:
        m = re.search(r'\bA\s*(\d)\b', combined, flags=re.IGNORECASE)
    if m:
        level_token = f"A{m.group(1)}"
    # detect alternance
    if re.search(r'\bALTERNANCE\b|\bAPPRENTICE\b|\bAPPRENTISSAGE\b', combined, flags=re.IGNORECASE):
        is_appr = True

    # determine school: take first token that is not "ANNEE" token and not major/alternance
    # assume first word(s) before 'ANNEE' are school name
    if re.search(r'\bANNEE\b', combined, flags=re.IGNORECASE):
        school = combined.split(re.search(r'\bANNEE\b', combined, flags=re.IGNORECASE).group(0))[0].strip(" -")
    else:
        # if parts length >=1, first part probably school
        school = parts[0].strip()

    # determine major: look for known pattern after ANNEE or last part that is not alternance
    # last part that is not "ALTERNANCE"
    for p in reversed(parts):
        if re.search(r'\bALTERNANCE\b|\bAPPRENTICE\b', p, flags=re.IGNORECASE):
            continue
        if re.search(r'\bANNEE\b|\bA\s*\d\b', p, flags=re.IGNORECASE):
            continue
        # if p contains school name only, skip
        if p.strip().lower() == school.strip().lower():
            continue
        major = p
        break

    # sanitize
    if school:
        school = re.sub(r'\bANNEE\b.*$', '', school, flags=re.IGNORECASE).strip(" -")
    if major:
        major = major.strip()

    return school or None, level_token or None, major or None, is_appr

def create_promotion_from_descriptor(db: Session, descriptor: str, year: Optional[int] = None) -> Promotion:
    school_name, level_token, major_name, is_appr = parse_descriptor(descriptor)
    if not school_name:
        raise ValueError("Cannot determine school from descriptor")

    # determine promotion year (use provided year or current calendar year)
    promotion_year = int(year) if year else date.today().year

    # ensure entities exist
    school = _get_or_create_school(db, school_name)
    level = _get_or_create_level(db, level_token or "A1")
    major = None
    if major_name:
        major = _get_or_create_major(db, major_name, school.id, level.id)

    # create promotion if not exists (unique semantics can vary; here check identical tuple)
    qry = db.query(Promotion).filter(
        Promotion.school_id == school.id,
        Promotion.level_id == level.id,
        Promotion.year == promotion_year,
        Promotion.major_id == (major.id if major else None),
        Promotion.is_apprentice == bool(is_appr)
    )
    existing = qry.first()
    if existing:
        return existing

    promo = Promotion(
        year=promotion_year,
        level_id=level.id,
        school_id=school.id,
        major_id=(major.id if major else None),
        is_apprentice=bool(is_appr)
    )
    db.add(promo)
    db.commit()
    db.refresh(promo)
    return promo