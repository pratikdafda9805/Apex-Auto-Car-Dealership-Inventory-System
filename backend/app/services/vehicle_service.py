from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.vehicle import Vehicle
from app.models.transaction import Transaction, TransactionTypeEnum
from app.schemas.vehicle import VehicleCreate, VehicleUpdate

class VehicleService:
    def __init__(self, db: Session):
        self.db = db

    def create_vehicle(self, vehicle_in: VehicleCreate) -> Vehicle:
        """Create a new vehicle record."""
        vehicle = Vehicle(**vehicle_in.model_dump())
        self.db.add(vehicle)
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def get_vehicle_by_id(self, vehicle_id: str) -> Optional[Vehicle]:
        """Fetch a single vehicle by ID."""
        return self.db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    def get_all_vehicles(self) -> List[Vehicle]:
        """Fetch all available vehicles."""
        return self.db.query(Vehicle).all()

    def search_vehicles(
        self,
        make: Optional[str] = None,
        model: Optional[str] = None,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> List[Vehicle]:
        """Search and filter vehicles by make, model, category, or price range."""
        query = self.db.query(Vehicle)

        if make:
            query = query.filter(Vehicle.make.ilike(f"%{make}%"))
        if model:
            query = query.filter(Vehicle.model.ilike(f"%{model}%"))
        if category:
            query = query.filter(Vehicle.category.ilike(f"%{category}%"))
        if min_price is not None:
            query = query.filter(Vehicle.price >= min_price)
        if max_price is not None:
            query = query.filter(Vehicle.price <= max_price)

        return query.all()

    def update_vehicle(self, vehicle_id: str, vehicle_in: VehicleUpdate) -> Vehicle:
        """Update an existing vehicle's details."""
        vehicle = self.get_vehicle_by_id(vehicle_id)
        if not vehicle:
            raise ValueError("Vehicle not found")

        update_data = vehicle_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(vehicle, field, value)

        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def delete_vehicle(self, vehicle_id: str) -> bool:
        """Delete a vehicle by ID."""
        vehicle = self.get_vehicle_by_id(vehicle_id)
        if not vehicle:
            raise ValueError("Vehicle not found")

        self.db.delete(vehicle)
        self.db.commit()
        return True

    def purchase_vehicle(self, vehicle_id: str, user_id: str, quantity: int) -> Tuple[Vehicle, Transaction]:
        """Purchase a vehicle, decreasing its stock quantity."""
        vehicle = self.get_vehicle_by_id(vehicle_id)
        if not vehicle:
            raise ValueError("Vehicle not found")

        if vehicle.quantity < quantity:
            raise ValueError("Insufficient stock available")

        vehicle.quantity -= quantity

        tx = Transaction(
            vehicle_id=vehicle.id,
            user_id=user_id,
            type=TransactionTypeEnum.PURCHASE,
            quantity=quantity
        )

        self.db.add(tx)
        self.db.commit()
        self.db.refresh(vehicle)
        self.db.refresh(tx)

        return vehicle, tx

    def restock_vehicle(self, vehicle_id: str, user_id: str, quantity: int) -> Tuple[Vehicle, Transaction]:
        """Restock a vehicle, increasing its stock quantity."""
        vehicle = self.get_vehicle_by_id(vehicle_id)
        if not vehicle:
            raise ValueError("Vehicle not found")

        vehicle.quantity += quantity

        tx = Transaction(
            vehicle_id=vehicle.id,
            user_id=user_id,
            type=TransactionTypeEnum.RESTOCK,
            quantity=quantity
        )

        self.db.add(tx)
        self.db.commit()
        self.db.refresh(vehicle)
        self.db.refresh(tx)

        return vehicle, tx
