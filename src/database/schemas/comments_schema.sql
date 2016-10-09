DROP TABLE IF EXISTS comments;

CREATE TABLE comments (
  comment_id INT NOT NULL,
  book_id INT NOT NULL,
  username VARCHAR(50),
  time DATE,
  rating INT NOT NULL,
  comment VARCHAR(5000),

  PRIMARY KEY(comment_id),
  FOREIGN KEY(book_id) REFERENCES books(book_id)
);
