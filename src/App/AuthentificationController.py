from typing import Literal, Optional

from fastapi import APIRouter, HTTPException, status

from src.App.init_app import customer_service, jwt_service, user_service
from src.Model.JWTResponse import JWTResponse

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    first_name: str,
    last_name: str,
    phone: str,
    mail: str,
    password: str,
    confirm_password: str,
    address_string: str,
):
    # Suggestion: registration has a field for each "component" of the address
    # Suggestion: login confirmation message using the returned dict
    # Question: what is expected to be caught in the ValueError and in the last Exception ?
    #           Why is is 2 different errors? Is ValueError for stuff caught in CustomerService
    #           And Exception for anything else ?
    # Question: why return the customer object content and the JWT ?
    #           what are they used for afterwards ?
    """
    Registration request for customers

    Parameters
    ----------
    first_name : str
        first name of the customer
    last_name : str
        last name of the customer
    phone : str
        phone number of the customer. Phone number validity is checked by CustomerService.
    mail : str
        email address of the customer
    password : str
        Password [TODO: specify requirements]
    confirm_password : str
        Password confirmation, must match password
    address_string : str
        Address of the customer as a string. Address validity is cheked by CustomerService.

    Returns
    -------
    _type_: ?
        _description_ : ?
    Raises
    ------
    HTTPException
        raised if password confimration field differs from password field
    HTTPException
        _description_ ?
    HTTPException
        _description_ ?
    """
    try:
        if confirm_password != password:
            raise HTTPException(status_code=400, detail="The two password don't match.")
        customer = customer_service.create_customer(
            first_name, last_name, phone, mail, password, address_string
        )

        jwt_token = jwt_service.encode_jwt(customer.id)

        return {
            "user": {
                "id": customer.id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "phone": customer.customer_phone,
                "email": customer.customer_mail,
                "hash_pw": customer.password,
                "type": "customer",
            },
            "access_token": jwt_token.access_token,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {e}") from e


@auth_router.post("/login", status_code=status.HTTP_200_OK)
def login(
    identifier: Optional[str], password: str, user_type: Literal["admin", "customer", "driver"]
) -> JWTResponse:
    """
    Login request for users regardless of type

    Parameters
    ----------
    identifier : Optional[str]
        For customers : email address or phone number
        For drivers : phone number
        For admins : None
    password : str
        Password of the user
    user_type : Literal[admin, customer, driver]
        Type of user

    Returns
    -------
    JWTResponse
       JWT token to allow further actions without re-login

    Raises
    ------
    HTTPException
        raised if invalid user type
    HTTPException
        raised if invalid credentials
    HTTPException
        other exceptions
    """
    try:
        if user_type not in ("admin", "customer", "driver"):
            raise HTTPException(
                status_code=400, detail="Invalid user_type. Must be: customer, driver, or admin"
            )

        user = user_service.login(identifier=identifier, password=password, user_type=user_type)

        token = jwt_service.encode_jwt(user.id)
        return token

    except ValueError as e:
        raise HTTPException(status_code=401, detail="Invalid credentials") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {e}") from e
