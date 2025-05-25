from sqlalchemy.orm import Session
from datetime import datetime
from app.models.assets import Asset
from app.schemas.assets import AssetCreate
from fastapi import HTTPException, status

class AssetCRUD:
    @staticmethod
    def create_asset(db: Session, asset: AssetCreate) -> Asset:
        # Get the last asset and extract the numeric part of the ID
        last_asset = db.query(Asset).order_by(Asset.id.desc()).first()
        
        if last_asset:
            try:
                # Try to extract number after 'AST'
                if last_asset.asset_id.startswith("AST"):
                    last_id = int(last_asset.asset_id[3:])
                    next_id = last_id + 1
                else:
                    # If the format is different, start with 1
                    next_id = 1
            except (ValueError, IndexError):
                # If there's any error parsing the ID, start with 1
                next_id = 1
        else:
            next_id = 1
        
        new_asset_id = f"AST{str(next_id).zfill(4)}"  # Format: AST0001, AST0002, etc.

        # Check if serial number already exists
        existing_serial_number = db.query(Asset).filter(Asset.serial_number == asset.serial_number).first()

        if existing_serial_number:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Asset with this Serial Number already exists"
            )

        db_asset = Asset(
            asset_id=new_asset_id,
            asset_name=asset.asset_name,
            value=asset.value,
            purchase_date=asset.purchase_date,
            manufacturer=asset.manufacturer,
            model=asset.model,
            serial_number=asset.serial_number,
            supplier=asset.supplier,
            warranty=asset.warranty,
            warranty_expiry=asset.warranty_expiry,
            status=asset.status,
            facility_name=asset.facility_name
        )
        
        db.add(db_asset)
        db.commit()
        db.refresh(db_asset)
        
        return db_asset

    @staticmethod
    def update_asset(db: Session, id: str, asset: AssetCreate) -> Asset:
        # Filter by asset_id (string) instead of id (integer)
        db_asset = db.query(Asset).filter(Asset.asset_id == id).first()
        if not db_asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        for key, value in asset.dict(exclude_unset=True).items():
            setattr(db_asset, key, value)
        
        db.commit()
        db.refresh(db_asset)
        return db_asset

    @staticmethod
    def delete_asset(db: Session, id: str) -> dict:
        # Filter by asset_id instead of id
        db_asset = db.query(Asset).filter(Asset.asset_id == id).first()
        if not db_asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        db.delete(db_asset)
        db.commit()
        return {"message": "Asset deleted successfully"}

    @staticmethod
    def get_asset_by_id(db: Session, id: str) -> Asset:
        # Filter by asset_id instead of id
        db_asset = db.query(Asset).filter(Asset.asset_id == id).first()
        if not db_asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        return db_asset

    @staticmethod
    def get_all_facility_names(db: Session) -> list:
        facility_names = db.query(Asset.facility_name).distinct().all()
        return [name[0] for name in facility_names]

    @staticmethod
    def get_all_assets(db: Session) -> list:
        return db.query(Asset).all()
