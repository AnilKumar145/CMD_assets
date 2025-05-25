from sqlalchemy import Column, Integer, String, Date, Numeric, Enum as SQLAlchemyEnum
from app.models.base import Base
from enum import Enum

class Status(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(String, nullable=False, unique=True)
    asset_name = Column(String, nullable=False)
    value = Column(Numeric, nullable=False)
    purchase_date = Column(Date, nullable=False)
    manufacturer = Column(String, nullable=False)
    model = Column(String, nullable=False)
    serial_number = Column(String, nullable=False, unique=True)
    supplier = Column(String, nullable=False)
    warranty = Column(Integer, nullable=False)  # in months
    warranty_expiry = Column(Date, nullable=False)
    status = Column(SQLAlchemyEnum(Status), default=Status.ACTIVE)
    facility_name = Column(String, nullable=False)

    def __repr__(self):
        return f"Asset(asset_id={self.asset_id}, name={self.asset_name})"
