from sqlalchemy import (
    BigInteger, Boolean, Column, String, Index, Integer, Date, DateTime,
    Text
)
from base_sqlalchemy import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
import datetime


# Swachh Manch user model
class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True)
    code = Column(String(30),)
    district_id = Column(Integer)
    district_title = Column(String(100))
    state_title = Column(String(100))
    state_id = Column(Integer)
    title = Column(String(100))
    latitude = Column(String(30))
    longitude = Column(String(30))
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    deleted = Column(Boolean, default=False, index=True)
    deleted_at = Column(DateTime)
    wards = relationship("Ward", back_populates="city")

# SM wards model
class Ward(Base):
    __tablename__ = 'wards_not_sync'

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('cities.id'), index=True, )
    city = relationship("City", back_populates="wards")
    ward_translations = relationship("WardTranslation", back_populates="ward")
    ward_number = Column(String(100), index=True)
    meta_data_ward_id = Column(Integer, index=True)
    meta_data_city_id = Column(Integer, index=True)
    meta_data_ward_number = Column(String(100), index=True)
    bound_id = Column(Integer)
    previous_rank = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime)

class WardTranslation(Base):
    __tablename__ = "ward_translations"

    id = Column(Integer, primary_key=True)
    ward_id = Column(Integer, ForeignKey('wards_not_sync.id'), index=True,)
    ward = relationship("Ward", back_populates="ward_translations")
    locale = Column(String(2), default="en")
    title = Column(String(255))


