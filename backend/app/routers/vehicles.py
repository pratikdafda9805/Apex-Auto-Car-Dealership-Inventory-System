from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.vehicle import VehicleCreate, VehicleUpdate, VehicleResponse, QuantityAction
from app.services.vehicle_service import VehicleService
from app.middleware.auth_middleware import get_current_user, require_admin

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.get("", response_model=List[VehicleResponse])
def get_vehicles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """View a list of all available vehicles (Protected)."""
    service = VehicleService(db)
    return service.get_all_vehicles()

@router.get("/search", response_model=List[VehicleResponse])
def search_vehicles(
    make: Optional[str] = Query(None, description="Make of the vehicle"),
    model: Optional[str] = Query(None, description="Model of the vehicle"),
    category: Optional[str] = Query(None, description="Category (Sedan, SUV, Truck, etc.)"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search for vehicles by make, model, category, or price range (Protected)."""
    service = VehicleService(db)
    return service.search_vehicles(
        make=make,
        model=model,
        category=category,
        min_price=min_price,
        max_price=max_price
    )

@router.post("", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    vehicle_in: VehicleCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """Add a new vehicle (Admin Only)."""
    service = VehicleService(db)
    return service.create_vehicle(vehicle_in)

@router.put("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(
    vehicle_id: str,
    vehicle_in: VehicleUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """Update a vehicle's details (Admin Only)."""
    service = VehicleService(db)
    try:
        return service.update_vehicle(vehicle_id, vehicle_in)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{vehicle_id}")
def delete_vehicle(
    vehicle_id: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """Delete a vehicle (Admin Only)."""
    service = VehicleService(db)
    try:
        service.delete_vehicle(vehicle_id)
        return {"message": "Vehicle deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/{vehicle_id}/purchase")
def purchase_vehicle(
    vehicle_id: str,
    action: QuantityAction,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Purchase a vehicle, decreasing its quantity (Protected)."""
    service = VehicleService(db)
    try:
        vehicle, tx = service.purchase_vehicle(vehicle_id, current_user.id, action.quantity)
        return {
            "message": f"Successfully purchased {action.quantity} vehicle(s)",
            "vehicle": VehicleResponse.model_validate(vehicle),
            "transaction_id": tx.id
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/{vehicle_id}/restock")
def restock_vehicle(
    vehicle_id: str,
    action: QuantityAction,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """Restock a vehicle, increasing its quantity (Admin Only)."""
    service = VehicleService(db)
    try:
        vehicle, tx = service.restock_vehicle(vehicle_id, current_admin.id, action.quantity)
        return {
            "message": f"Successfully restocked {action.quantity} vehicle(s)",
            "vehicle": VehicleResponse.model_validate(vehicle),
            "transaction_id": tx.id
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
