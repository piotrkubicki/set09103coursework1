DROP TABLE if EXISTS genres;

CREATE TABLE genres (
  genre_id int NOT NULL,
  name varchar(30) NOT NULL,
  PRIMARY KEY (genre_id)
);
