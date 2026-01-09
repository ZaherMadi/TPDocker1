CREATE TABLE IF NOT EXISTS students
(
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    promo VARCHAR(50) NOT NULL
);

INSERT INTO students (nom, promo) VALUES
('Zaher Madi', 'M2 Dev 2526'),
('Nadjide', 'M2 Dev 2526'),
('Nawfel', 'M2 Dev 2526'),
('Adam ', 'M2 Dev 2526'),
('Toto Tutu', 'M2 Dev 2526'),
('Peppa Pig', 'M2 Dev 2526'); 