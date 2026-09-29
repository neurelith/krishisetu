"""
models.py — SQLAlchemy ORM models
"""
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class Farmer(Base):
    __tablename__ = "farmers"

    id          = Column(Integer, primary_key=True, index=True)
    grower_id   = Column(String, unique=True, index=True, nullable=False)
    name        = Column(String, nullable=True)
    age         = Column(Float, nullable=True)
    farm_size   = Column(Float, nullable=True)
    state       = Column(String, nullable=True)
    district    = Column(String, nullable=True)
    tehsil_block = Column(String, nullable=True)
    village     = Column(String, nullable=True)
    language    = Column(String, nullable=True)
    device_type = Column(String, nullable=True)
    connectivity = Column(String, nullable=True)
    literacy_level = Column(String, nullable=True)
    gender      = Column(String, nullable=True)
    crop        = Column(String, nullable=True)          # main_crop
    high_value_farmer = Column(Boolean, default=False)

    # Raw crop calendar JSON for feature engineering
    crop_calendar_json = Column(Text, nullable=True)

    # Static behavioural flags
    product_scan              = Column(Boolean, default=False)
    offline_campaign_attended = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    campaigns   = relationship("Campaign",   back_populates="farmer")
    predictions = relationship("Prediction", back_populates="farmer")
    advisories  = relationship("Advisory", back_populates="farmer")


class Campaign(Base):
    __tablename__ = "campaigns"

    id               = Column(Integer, primary_key=True, index=True)
    farmer_id        = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    product          = Column(String, nullable=True)
    campaign_crop    = Column(String, nullable=True)
    channel          = Column(String, nullable=True)
    message          = Column(Text, nullable=True)
    sms_message      = Column(Text, nullable=True)
    whatsapp_message = Column(Text, nullable=True)
    voice_script     = Column(Text, nullable=True)
    rag_summary      = Column(Text, nullable=True)
    predicted_score  = Column(Float, nullable=True)
    segment          = Column(String, nullable=True)
    actual_clicked   = Column(Boolean, nullable=True)
    audio_file       = Column(String, nullable=True)
    sent_at          = Column(DateTime, nullable=True)
    created_at       = Column(DateTime, default=datetime.utcnow)

    farmer = relationship("Farmer", back_populates="campaigns")


class Prediction(Base):
    __tablename__ = "predictions"

    id                     = Column(Integer, primary_key=True, index=True)
    farmer_id              = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    engagement_probability = Column(Float, nullable=False)
    segment                = Column(String, nullable=False)
    confidence             = Column(String, nullable=True)
    campaign_product       = Column(String, nullable=True)
    campaign_crop          = Column(String, nullable=True)
    primary_channel        = Column(String, nullable=True)
    primary_message        = Column(Text, nullable=True)
    rag_summary            = Column(Text, nullable=True)
    model_version          = Column(String, nullable=True)
    created_at             = Column(DateTime, default=datetime.utcnow)

    farmer = relationship("Farmer", back_populates="predictions")


class Advisory(Base):
    __tablename__ = "advisories"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    crop = Column(String, nullable=True)
    pest_threat = Column(String, nullable=True)
    language = Column(String, nullable=True)
    channel = Column(String, nullable=True)
    sms = Column(Text, nullable=True)
    whatsapp = Column(Text, nullable=True)
    voice_script = Column(Text, nullable=True)
    audio_file = Column(String, nullable=True)
    rag_sources_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    farmer = relationship("Farmer", back_populates="advisories")
