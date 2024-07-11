from fastapi import APIRouter

router = APIRouter()

@router.get("/check-subscription")
def check_subscription():
    return {"message": "Subscription checked"}
