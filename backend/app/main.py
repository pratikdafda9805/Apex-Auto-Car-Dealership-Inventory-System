from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base, SessionLocal
from app.routers import auth, vehicles
from app.models.user import User, RoleEnum
from app.models.vehicle import Vehicle
from app.utils.password_utils import hash_password

def create_tables():
    Base.metadata.create_all(bind=engine)

def seed_initial_data():
    """Seeds default admin user and inventory items if the database is fresh."""
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == "admin@dealership.com").first()
        if not admin:
            admin_user = User(
                name="System Admin",
                email="admin@dealership.com",
                password=hash_password("Admin@123"),
                role=RoleEnum.ADMIN
            )
            db.add(admin_user)

        user = db.query(User).filter(User.email == "user@dealership.com").first()
        if not user:
            regular_user = User(
                name="John Customer",
                email="user@dealership.com",
                password=hash_password("User@123"),
                role=RoleEnum.USER
            )
            db.add(regular_user)

        if db.query(Vehicle).count() == 0:
            sample_vehicles = [
                Vehicle(make="Toyota", model="Camry", year=2024, category="Sedan", price=28500.0, quantity=5, color="Midnight Black", mileage=10),
                Vehicle(make="Honda", model="CR-V", year=2024, category="SUV", price=32000.0, quantity=3, color="Sonic Gray", mileage=25),
                Vehicle(make="Ford", model="Mustang GT", year=2023, category="Sports", price=48000.0, quantity=2, color="Race Red", mileage=120),
                Vehicle(make="Tesla", model="Model Y", year=2024, category="EV", price=44990.0, quantity=4, color="Pearl White", mileage=5),
                Vehicle(make="Chevrolet", model="Silverado 1500", year=2023, category="Truck", price=52000.0, quantity=0, color="Summit White", mileage=450),
            ]
            db.add_all(sample_vehicles)

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"[startup] Failed to seed database: {e}")
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    seed_initial_data()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(vehicles.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"status": "healthy", "service": settings.PROJECT_NAME}

