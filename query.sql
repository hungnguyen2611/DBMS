------- Query on Book ------
SELECT * from Book;
SELECT * from Author;
--- Fitler book which have rating from 3->4, using index ----
SELECT * from Book WHERE avg_rating BETWEEN 3 AND 4;
--- Query on Author who start with "Diana" ----
SELECT * from Author WHERE name LIKE 'Diana%';
--- Query on Book whose'title start with "Lights" ----
SELECT * from Book WHERE title LIKE 'Lights%';
----Find all books which have publish_year is 2020 ----
SELECT * from Book WHERE publish_year = 2020;

---- List all genres of the book 'The Cousins' -------
SELECT name FROM Genre g JOIN Book_Genre bg ON g.id = bg.genre_id  
    WHERE bg.book_id = (SELECT id from Book WHERE title = 'The Cousins');