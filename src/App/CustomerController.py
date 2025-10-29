from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from src.Model.APIUser import APIUser
from src.Model.JWTResponse import JWTResponse
from src.Service.PasswordService import check_password_strength, validate_username_password

from .init_app import jwt_service, user_repo, user_service
from .JWTBearer import CustomerBearer

if TYPE_CHECKING:
    from src.Model.Customer import Customer


customer_router = APIRouter(prefix="/customer", tags=["Customers"])
