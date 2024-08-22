from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from src.db.connection import aget_connection, release_connection
from src.app.api.reviews.schema import ReviewCreate, Review
from src.app.api.auth.utils import auth_utils
from src.db.models.user import User

router = APIRouter()

@router.post("/{book_id}/reviews", response_model=Review)
async def create_review(book_id: int, review: ReviewCreate, current_user: User = Depends(auth_utils.get_current_user)):
    print(current_user)
    review.user_id = current_user.get("id")
    conn = await aget_connection()
    try:
        result = await conn.fetchrow(
            """
            INSERT INTO jktech.reviews (book_id, user_id, review_text, rating)
            VALUES ($1, $2, $3, $4)
            RETURNING id, book_id, user_id, review_text, rating
            """,
            book_id, review.user_id, review.review_text, review.rating
        )
        return Review(**result)
    finally:
        await release_connection(conn)

@router.get("/{book_id}/reviews", response_model=List[Review])
async def get_reviews(book_id: int, current_user: User = Depends(auth_utils.get_current_user)):
    print(current_user)
    conn = await aget_connection()
    try:
        results = await conn.fetch(
            """
            SELECT id, book_id, user_id, review_text, rating
            FROM jktech.reviews
            WHERE book_id = $1
            """,
            book_id
        )
        return [Review(**record) for record in results]
    finally:
        await release_connection(conn)

@router.get("/{book_id}/summary", response_model=Optional[dict])
async def get_book_summary(book_id: int, current_user: User = Depends(auth_utils.get_current_user)):
    print(current_user)
    conn = await aget_connection()
    try:
        # Get book summary and aggregated rating
        result = await conn.fetchrow(
            """
            SELECT b.title, b.author, b.genre, b.year_published, b.summary,
                   COALESCE(AVG(r.rating), 0) AS avg_rating
            FROM jktech.books b
            LEFT JOIN jktech.reviews r ON b.id = r.book_id
            WHERE b.id = $1
            GROUP BY b.id
            """,
            book_id
        )
        if not result:
            raise HTTPException(status_code=404, detail="Book not found")

        return {
            "title": result["title"],
            "author": result["author"],
            "genre": result["genre"],
            "year_published": result["year_published"],
            "summary": result["summary"],
            "avg_rating": result["avg_rating"]
        }
    finally:
        await release_connection(conn)