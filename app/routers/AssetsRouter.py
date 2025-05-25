from fastapi import APIRouter, Depends, Security, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.assets import AssetCreate, AssetResponse, FacilityNamesResponse
from app.database import get_db
from app.AssetsCrud import AssetCRUD
from app.auth_utils import get_current_user, get_admin_user, get_staff_user, User

# Restore the original router configuration
router = APIRouter(
    tags=["assets"]
)

@router.post("/addAsset", response_model=AssetResponse)
def create_asset(
    asset: AssetCreate, 
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_user, scopes=["ADMIN", "STAFF"])
):
    """
    Create a new asset with the following information:
    
    - **asset_name**: Name of the asset
    - **value**: Monetary value of the asset
    - **purchase_date**: Date when the asset was purchased
    - **manufacturer**: Manufacturer of the asset
    - **model**: Model number or name
    - **serial_number**: Unique serial number (must be unique)
    - **supplier**: Supplier or vendor name
    - **warranty**: Warranty period in months
    - **warranty_expiry**: Date when warranty expires
    - **status**: Current status (e.g., "Active", "Maintenance", "Retired")
    - **facility_name**: Name of the facility where the asset is located
    
    Returns the created asset with its generated asset_id.
    
    Requires ADMIN or STAFF role.
    """
    return AssetCRUD.create_asset(db, asset)

@router.patch("/{id}", response_model=AssetResponse)
def update_asset(
    id: str, 
    asset: AssetCreate, 
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_user, scopes=["ADMIN", "STAFF"])
):
    """
    Update an existing asset by its asset_id.
    
    - **id**: The asset_id of the asset to update (e.g., "AST0001")
    - Request body: Same as for creating an asset, but fields are optional
    
    Returns the updated asset if found, otherwise returns a 404 error.
    
    Requires ADMIN or STAFF role.
    """
    return AssetCRUD.update_asset(db, id, asset)

@router.delete("/{id}", response_model=None)
def delete_asset(
    id: str, 
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_user, scopes=["ADMIN"])
):
    """
    Delete an asset by its asset_id.
    
    - **id**: The asset_id of the asset to delete (e.g., "AST0001")
    
    Returns a success message if the asset was deleted, otherwise returns a 404 error.
    
    Requires ADMIN role.
    """
    return AssetCRUD.delete_asset(db, id)

@router.get("/{id}", response_model=AssetResponse)
def get_asset_by_id(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific asset by its asset_id.
    
    - **id**: The asset_id of the asset to retrieve (e.g., "AST0001")
    
    Returns the asset if found, otherwise returns a 404 error.
    
    Accessible to all authenticated users.
    """
    return AssetCRUD.get_asset_by_id(db, id)

@router.get("/facility/names", response_model=FacilityNamesResponse)
def get_all_facility_names(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a list of all unique facility names used in assets.
    
    Returns a list of facility names wrapped in a FacilityNamesResponse object.
    
    Accessible to all authenticated users.
    """
    facility_names = AssetCRUD.get_all_facility_names(db)
    return FacilityNamesResponse(facility_names=facility_names)

@router.get("/get/all", response_model=List[AssetResponse])
def get_all_assets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return"),
    status: Optional[str] = Query(None, description="Filter by asset status"),
    facility: Optional[str] = Query(None, description="Filter by facility name")
):
    """
    Get all assets with optional filtering and pagination.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    - **status**: Filter assets by status (e.g., "Active", "Maintenance")
    - **facility**: Filter assets by facility name
    
    Returns a list of assets matching the criteria.
    
    Accessible to all authenticated users.
    """
    assets = AssetCRUD.get_all_assets(db)
    
    # Apply filters if provided
    if status:
        assets = [a for a in assets if a.status == status]
    if facility:
        assets = [a for a in assets if a.facility_name == facility]
    
    # Apply pagination
    return assets[skip:skip+limit]
