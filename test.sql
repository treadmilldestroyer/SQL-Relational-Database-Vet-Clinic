
-- CREATE creates things like a table
-- here I created a table named Authors
CREATE TABLE Authors (
    -- PRIMARY KEY is the identifier for each entry in the table. 
    -- Choose this identifier wisely according to the data type.
    -- this PRIMARY KEY is by best practice listed first in a table.
    AuthorID INTEGER PRIMARY KEY AUTOINCREMENT, 
    -- this AUTOINCREMENT will automatically place a new PRIMARY KEY number 
    -- (since it's an INT) for us
    FullName TEXT,
    Nationality TEXT
);

-- here I created another table named Books
CREATE TABLE Books (
    BookID INT PRIMARY KEY,
    Title TEXT,
    Genre TEXT,
    AuthorID INT,
    FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID)
);

INSERT INTO Authors (AuthorID, FullName, Nationality)
VALUES (1, 'J.K. Rowling', 'British');

INSERT INTO Books (BookID, Title, Genre, AuthorID)
VALUES (101, 'Harry Potter', 'Fantasy', 1);

SELECT * FROM Books; -- this SELECT command pulls data
SELECT * FROM Authors;