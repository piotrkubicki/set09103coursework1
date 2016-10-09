DROP TABLE IF EXISTS book_author;

CREATE TABLE book_author (
  book_id INT NOT NULL,
  author_id INT NOT NULL,

  FOREIGN KEY(book_id) REFERENCES books(book_id),
  FOREIGN KEY(author_id) REFERENCES authors(author_id)
);
