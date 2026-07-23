from sqlalchemy.orm import Session
from app.models.user import User, RoleEnum
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserResponse
from app.utils.password_utils import hash_password, verify_password
from app.utils.jwt_utils import create_access_token

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, user_data: UserRegister) -> TokenResponse:
        """Register a new user, hash password, save to DB, and return token + user info."""
        existing_user = self.db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise ValueError("User with this email already exists")

        hashed_pwd = hash_password(user_data.password)
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password=hashed_pwd,
            role=user_data.role or RoleEnum.USER
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        user_resp = UserResponse.model_validate(new_user)
        token_payload = {"sub": new_user.id, "email": new_user.email, "role": new_user.role.value}
        access_token = create_access_token(token_payload)

        return TokenResponse(access_token=access_token, token_type="bearer", user=user_resp)

    def login(self, login_data: UserLogin) -> TokenResponse:
        """Authenticate user by email/password and return access token."""
        user = self.db.query(User).filter(User.email == login_data.email).first()
        if not user or not verify_password(login_data.password, user.password):
            raise ValueError("Invalid email or password")

        user_resp = UserResponse.model_validate(user)
        token_payload = {"sub": user.id, "email": user.email, "role": user.role.value}
        access_token = create_access_token(token_payload)

        return TokenResponse(access_token=access_token, token_type="bearer", user=user_resp)
