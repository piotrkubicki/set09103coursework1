DROP TABLE if EXISTS authors;

CREATE TABLE authors (
  author_id INT NOT NULL,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  date_of_birth DATE,
  date_of_dead DATE
);
