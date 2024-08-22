CREATE TABLE jktech.books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    year_published INT CHECK (year_published >= 1000 AND year_published <= EXTRACT(YEAR FROM CURRENT_DATE)),
    summary TEXT
);

CREATE TABLE jktech.reviews (
    id SERIAL PRIMARY KEY,
    book_id INT REFERENCES jktech.books(id) ON DELETE CASCADE,
    user_id INT NOT NULL,
    review_text TEXT,
    rating INT CHECK (rating >= 1 AND rating <= 5)
);

CREATE TABLE jktech.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_datetime TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    last_login_time TIMESTAMPTZ
);

