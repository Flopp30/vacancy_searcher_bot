from fastapi import APIRouter

from app.endpoints.profile import router as profile_router


main_router = APIRouter()
main_router.include_router(
    profile_router,
    prefix='/profile',
    tags=['User profile']
)
