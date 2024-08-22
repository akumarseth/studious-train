from fastapi.routing import APIRouter
from src.app.api.auth.view import router as auth_router
from src.app.api.books.views import router as books_router
from src.app.api.reviews.views import router as reviews_router


api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"], )
api_router.include_router(books_router, prefix="/books", tags=["Books"])
api_router.include_router(reviews_router, prefix="/books", tags=["Reviews"])
