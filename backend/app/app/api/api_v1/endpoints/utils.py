from typing import Any

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app.db_models.user.user import User
from app.models.msg import Msg
from app.api import deps
from app.utils import send_test_email

router = APIRouter()

@router.post("/test-email/", response_model=Msg, status_code=201)
def test_email(
    email_to: EmailStr,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}
