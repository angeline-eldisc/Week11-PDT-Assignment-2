-- Create table users
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
	email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP NULL DEFAULT NULL
);

-- Create table articles
DROP TABLE IF EXISTS articles;
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    user_id INT,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP NULL DEFAULT NULL,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Insert new data to users table
INSERT INTO users (username, name, email, password) VALUES ('admin', 'Administrator', 'admin@mail.com', 'admin');
INSERT INTO users (username, name, email, password) VALUES ('john', 'John Doe', 'john@mail.com', 'john');

-- Insert new data to articles table
INSERT INTO articles (title, body, user_id) VALUES
    ('C Programming Language', 'C was originally developed at Bell Labs by Dennis Ritchie between 1972 and 1973', 1),
    ('Python Programming Language', 'Python was conceived in the late 1980s by Guido van Rossum at Centrum Wiskunde & Informatica (CWI) in the Netherlands.', 2),
    ('Java Programming Language', 'Java was originally developed by James Gosling at Sun Microsystems and released in May 1995', 1),
    ('PHP Programming Language', 'PHP was originally created by Danish-Canadian programmer Rasmus Lerdorf in 1994.', 1),
    ('Lua Programming Language', 'Lua was created in 1993 by Roberto Ierusalimschy, Luiz Henrique de Figueiredo, and Waldemar Celes, members of the Computer Graphics Technology Group (Tecgraf) at the Pontifical Catholic University of Rio de Janeiro, in Brazil.', 2)
;