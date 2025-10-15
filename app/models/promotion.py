from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Promotion(Base):
    __tablename__ = "promotion"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    level_id = Column(Integer, ForeignKey("level.id"), nullable=False)
    school_id = Column(Integer, ForeignKey("school.id"), nullable=False)
    major_id = Column(Integer, ForeignKey("major.id"), nullable=True)
    is_apprentice = Column(Boolean, nullable=False)

    # Relationships so nested attributes are available for Pydantic's from_attributes
    level = relationship("Level", lazy="joined")
    school = relationship("School", lazy="joined")
    major = relationship("Major", lazy="joined")

    def __repr__(self):
        return f"<Promotion id={self.id} year={self.year} school_id={self.school_id} level_id={self.level_id} major_id={self.major_id}>"
