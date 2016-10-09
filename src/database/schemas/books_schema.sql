DROP TABLE IF EXISTS books;

CREATE TABLE books (
  book_id int NOT NULL,
  title VARCHAR(100) NOT NULL,
  year VARCHAR(4),
  publisher VARCHAR(50),
  cover VARCHAR(255),
  genre_id int NOT NULL,
  pages int,

  PRIMARY KEY (book_id),
  FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);
