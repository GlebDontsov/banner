from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    func
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    """Базовый класс."""


class Banner(Base):
    """Таблица Banner."""

    __tablename__ = 'banner'

    id = Column(Integer, primary_key=True)
    feature_id = Column(Integer)
    tag_ids = Column(ARRAY(Integer))  # type: ignore
    title = Column(String(500))
    text = Column(String(5000))
    url = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now())

    banner_tags_features = relationship(
        'BannerTagsFeature',
        back_populates='banner',
        cascade='all, delete',
    )


class BannerTagsFeature(Base):
    """Таблица BannerTagsFeature."""

    __tablename__ = 'banner_tags_features'

    id = Column(Integer, primary_key=True)
    banner_id = Column(Integer, ForeignKey('banner.id'))
    feature_id = Column(Integer)
    tag_ids = Column(Integer)

    banner = relationship('Banner', back_populates='banner_tags_features')
