from fastapi import APIRouter, Depends, Request, HTTPException
from typing import List, Optional
from src.app.api.books import ollama_summarization
from src.db.connection import aget_connection, release_connection
from src.app.api.books.schema import BookContentRequest, BookCreate, Book
from src.app.api.auth.utils import auth_utils
from src.db.models.user import User
import pickle
import difflib
import os
from src.app.api.books.azure_helper import Azure_helper

router = APIRouter()

# Create a new book
@router.post("/", response_model=Book)
async def create_book(book: BookCreate, current_user: User = Depends(auth_utils.get_current_user)):
    print(current_user)
    conn = await aget_connection()
    try:
        result = await conn.fetchrow(
            """
            INSERT INTO jktech.books (title, author, genre, year_published, summary)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id, title, author, genre, year_published, summary
            """,
            book.title, book.author, book.genre, book.year_published, book.summary
        )
        return Book(**result)
    finally:
        await release_connection(conn)

# Retrieve all books
@router.get("/", response_model=List[Book])
async def get_books(request: Request, current_user: User = Depends(auth_utils.get_current_user)):
    print(current_user)
    conn = await aget_connection()
    try:
        results = await conn.fetch(
            """
            SELECT id, title, author, genre, year_published, summary
            FROM jktech.books
            """
        )
        return [Book(**record) for record in results]
    finally:
        await release_connection(conn)

# Retrieve a specific book by ID
@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int, current_user: User = Depends(auth_utils.get_current_user)):
    print(current_user)
    conn = await aget_connection()
    try:
        result = await conn.fetchrow(
            """
            SELECT id, title, author, genre, year_published, summary
            FROM jktech.books
            WHERE id = $1
            """,
            book_id
        )
        if not result:
            raise HTTPException(status_code=404, detail="Book not found")
        return Book(**result)
    finally:
        await release_connection(conn)

# Update a book by ID
@router.put("/{book_id}", response_model=Book)
async def update_book(book_id: int, book: BookCreate, current_user: User = Depends(auth_utils.get_current_user)):
    print(current_user)
    conn = await aget_connection()
    try:
        result = await conn.fetchrow(
            """
            UPDATE jktech.books
            SET title = $1, author = $2, genre = $3, year_published = $4, summary = $5
            WHERE id = $6
            RETURNING id, title, author, genre, year_published, summary
            """,
            book.title, book.author, book.genre, book.year_published, book.summary, book_id
        )
        if not result:
            raise HTTPException(status_code=404, detail="Book not found")
        return Book(**result)
    finally:
        await release_connection(conn)

# Delete a book by ID
@router.delete("/{book_id}")
async def delete_book(book_id: int, current_user: User = Depends(auth_utils.get_current_user)):
    print(current_user)
    conn = await aget_connection()
    try:
        result = await conn.execute(
            """
            DELETE FROM jktech.books
            WHERE id = $1
            """,
            book_id
        )
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Book not found")
        return {"message": "Book deleted successfully"}
    finally:
        await release_connection(conn)



@router.post("/generate_summary/{book_id}", response_model=Book)
async def generate_summary(book_id: int, bookContentRequest: BookContentRequest, current_user: User = Depends(auth_utils.get_current_user)):
    conn = await aget_connection()
    try:
        decoded_content = ollama_summarization.decode_base64(bookContentRequest.content)
        summary = await ollama_summarization.generate_summary(decoded_content)

        result = await conn.fetchrow(
            """
            UPDATE jktech.books
            SET summary = $1
            WHERE id = $2
            RETURNING id, title, author, genre, year_published, summary
            """,
            summary, book_id
        )
        if not result:
            raise HTTPException(status_code=404, detail="Book not found")
        return Book(**result)
    except Exception as e:
        print(e)
    finally:
        await release_connection(conn)


@router.get("/recommend_books/")
def recommend_books(user_genre: str, user_avg_rating: float):

    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # model_path = os.path.join(current_dir, 'model_data.pkl')

    az_helper = Azure_helper()
    model_path = az_helper.download_model_to_local_dir()

    try:
        with open(model_path, 'rb') as file:
            model_data = pickle.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail=f"Model file not found at {model_path}")


    df = model_data['df']
    similarity = model_data['similarity']
    list_of_all_genre = model_data['list_of_all_genre']
    list_of_all_avg_rating = model_data['list_of_all_avg_rating']
    
    # Find the closest match for genre
    closest_genre = difflib.get_close_matches(user_genre, list_of_all_genre, n=1)
    if not closest_genre:
        raise HTTPException(status_code=404, detail="No close match found for the provided genre.")
    
    # Find the closest match for average rating
    closest_avg_rating = difflib.get_close_matches(str(user_avg_rating), list(map(str, list_of_all_avg_rating)), n=1)
    if not closest_avg_rating:
        raise HTTPException(status_code=404, detail="No close match found for the provided average rating.")
    
    matched_genre = closest_genre[0]
    matched_avg_rating = float(closest_avg_rating[0])

    # Filter DataFrame for matching genre and average rating
    filtered_df = df[(df['genre'] == matched_genre) & (df['average_rating'] == matched_avg_rating)]
    if filtered_df.empty:
        raise HTTPException(status_code=404, detail="No books found matching the genre and average rating.")
    
    # Get the first match's index
    index_of_the_book = filtered_df.index[0]
    similarity_score = list(enumerate(similarity[index_of_the_book]))

    # Sort and get the top similar books
    sorted_similar_books = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    top_sim = sorted_similar_books[:10]

    # Retrieve the titles of similar books
    recommended_books = [df.iloc[book[0]]['title'] for book in top_sim]
    
    return {"recommended_books": recommended_books}
