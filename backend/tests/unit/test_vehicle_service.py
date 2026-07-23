import pytest
from app.services.vehicle_service import VehicleService
from app.schemas.vehicle import VehicleCreate, VehicleUpdate
from app.models.user import User, RoleEnum
from app.models.transaction import TransactionTypeEnum

@pytest.fixture
def sample_user(db_session):
    user = User(
        name="Buyer Bob",
        email="bob@example.com",
        password="hashedpassword",
        role=RoleEnum.USER
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def sample_admin(db_session):
    admin = User(
        name="Admin Alice",
        email="alice@example.com",
        password="hashedpassword",
        role=RoleEnum.ADMIN
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin

def test_create_vehicle_success(db_session):
    service = VehicleService(db_session)
    vehicle_in = VehicleCreate(
        make="Toyota",
        model="Camry",
        year=2024,
        category="Sedan",
        price=28000.0,
        quantity=5,
        color="Black",
        mileage=15
    )
    vehicle = service.create_vehicle(vehicle_in)
    assert vehicle.id is not None
    assert vehicle.make == "Toyota"
    assert vehicle.quantity == 5

def test_get_all_vehicles_returns_list(db_session):
    service = VehicleService(db_session)
    service.create_vehicle(VehicleCreate(make="Toyota", model="Camry", year=2024, category="Sedan", price=28000.0, quantity=5))
    service.create_vehicle(VehicleCreate(make="Ford", model="Mustang", year=2023, category="Sports", price=45000.0, quantity=2))
    
    vehicles = service.get_all_vehicles()
    assert len(vehicles) == 2

def test_search_vehicles_by_filters(db_session):
    service = VehicleService(db_session)
    service.create_vehicle(VehicleCreate(make="Toyota", model="Camry", year=2024, category="Sedan", price=28000.0, quantity=5))
    service.create_vehicle(VehicleCreate(make="Honda", model="Civic", year=2023, category="Sedan", price=25000.0, quantity=3))
    service.create_vehicle(VehicleCreate(make="Ford", model="F-150", year=2024, category="Truck", price=55000.0, quantity=1))

    # Filter by make
    res_make = service.search_vehicles(make="toyota")
    assert len(res_make) == 1
    assert res_make[0].make == "Toyota"

    # Filter by category
    res_cat = service.search_vehicles(category="Sedan")
    assert len(res_cat) == 2

    # Filter by price range
    res_price = service.search_vehicles(min_price=20000.0, max_price=30000.0)
    assert len(res_price) == 2
    assert all(20000 <= v.price <= 30000 for v in res_price)

def test_update_vehicle_success(db_session):
    service = VehicleService(db_session)
    v = service.create_vehicle(VehicleCreate(make="Toyota", model="Camry", year=2024, category="Sedan", price=28000.0, quantity=5))
    
    updated = service.update_vehicle(v.id, VehicleUpdate(price=26500.0, color="Silver"))
    assert updated.price == 26500.0
    assert updated.color == "Silver"

def test_update_nonexistent_vehicle_raises_value_error(db_session):
    service = VehicleService(db_session)
    with pytest.raises(ValueError, match="Vehicle not found"):
        service.update_vehicle("non-existent-id", VehicleUpdate(price=30000.0))

def test_delete_vehicle_success(db_session):
    service = VehicleService(db_session)
    v = service.create_vehicle(VehicleCreate(make="Toyota", model="Camry", year=2024, category="Sedan", price=28000.0, quantity=5))
    
    deleted = service.delete_vehicle(v.id)
    assert deleted is True
    assert service.get_vehicle_by_id(v.id) is None

def test_purchase_vehicle_decrements_quantity(db_session, sample_user):
    service = VehicleService(db_session)
    v = service.create_vehicle(VehicleCreate(make="Toyota", model="Camry", year=2024, category="Sedan", price=28000.0, quantity=5))
    
    v_updated, tx = service.purchase_vehicle(v.id, user_id=sample_user.id, quantity=2)
    assert v_updated.quantity == 3
    assert tx.type == TransactionTypeEnum.PURCHASE
    assert tx.quantity == 2

def test_purchase_vehicle_insufficient_stock_raises_value_error(db_session, sample_user):
    service = VehicleService(db_session)
    v = service.create_vehicle(VehicleCreate(make="Toyota", model="Camry", year=2024, category="Sedan", price=28000.0, quantity=1))
    
    with pytest.raises(ValueError, match="Insufficient stock available"):
        service.purchase_vehicle(v.id, user_id=sample_user.id, quantity=2)

def test_purchase_zero_stock_raises_value_error(db_session, sample_user):
    service = VehicleService(db_session)
    v = service.create_vehicle(VehicleCreate(make="Toyota", model="Camry", year=2024, category="Sedan", price=28000.0, quantity=0))
    
    with pytest.raises(ValueError, match="Insufficient stock available"):
        service.purchase_vehicle(v.id, user_id=sample_user.id, quantity=1)

def test_restock_vehicle_increments_quantity(db_session, sample_admin):
    service = VehicleService(db_session)
    v = service.create_vehicle(VehicleCreate(make="Toyota", model="Camry", year=2024, category="Sedan", price=28000.0, quantity=2))
    
    v_updated, tx = service.restock_vehicle(v.id, user_id=sample_admin.id, quantity=10)
    assert v_updated.quantity == 12
    assert tx.type == TransactionTypeEnum.RESTOCK
    assert tx.quantity == 10
