-- SETUP --
------------ CREATE DATABASE SCHEMA  -------
USE master;  
GO  
CREATE DATABASE DBMS_PROJECT 
ON PRIMARY
( NAME = DBMS_PROJECT_dat,  
    FILENAME = '/var/opt/mssql/data/dbms_data.mdf',  
    SIZE = 40,  
    MAXSIZE = 50,  
    FILEGROWTH = 5 )  
LOG ON  
( NAME = DBMS_PROJECT_log,  
    FILENAME = '/var/opt/mssql/log/dbms_datalog.ldf',  
    SIZE = 5MB,  
    MAXSIZE = 25MB,  
    FILEGROWTH = 5MB );  
GO

-------------- CREATE TABLE ----------------
CREATE TABLE Author(
    id INT NOT NULL PRIMARY KEY,
    name NVARCHAR(100),
    birth_date DATETIME,
    death_date DATETIME,
    about VARCHAR(5000)
);
GO


CREATE TABLE Book (
    id INT NOT NULL unique,
    author_id INT NOT NULL,
    url VARCHAR(255),
    title NVARCHAR(255),
    num_ratings INT,
    avg_rating FLOAT,
    language VARCHAR(16),
    publish_day INT,
    publish_month INT,
    publish_year INT,
    FOREIGN KEY (author_id) REFERENCES Author(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
);
GO


CREATE TABLE Genre(
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(50)
);
GO



CREATE TABLE Book_Genre(
    book_id INT NOT NULL,
    genre_id INT NOT NULL,
    FOREIGN KEY (book_id) REFERENCES Book(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES Genre(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);
GO


------ Indexing on Book --------
CREATE CLUSTERED INDEX avg_rating_index ON Book (avg_rating);
CREATE INDEX IX_title_index ON Book(title);
CREATE NONCLUSTERED INDEX id_index ON Book (id);
CREATE INDEX publish_year_index ON Book (publish_year);
------- Indexing on Author -----
CREATE INDEX IX_name_index ON Author(name);





-------- DROP TABLE ---------------
-- DROP TABLE Book;
-- DROP TABLE Author;
-- DROP TABLE Book_Genre;
-- DROP TABLE Genre;
-------------------------------------------------------------------











---------------------- Done --------------------

























