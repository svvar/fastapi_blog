from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import UserCreate, Token
from app.db.crud.user_crud import authenticate_user, create_user, check_user_exists
from app.db.session import get_db
from app.core.security import create_access_token

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
        user: UserCreate,
        db=Depends(get_db)
):
    if check_user_exists(db, user.email.strip()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")

    create_user(db, user)
    return {'msg': 'User created successfully'}



@router.post("/login", response_model=Token)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db=Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    access_token = create_access_token(
        data={"sub": user.email, "id": user.id}
    )
    return Token(access_token=access_token)



