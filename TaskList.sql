CREATE DATABASE IF NOT EXISTS tasklist;

USE tasklist;

CREATE TABLE TaskList
(
    Id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200),
    description TEXT,
    created_at DATETIME,
    updated_at DATETIME
);

INSERT INTO TaskList (title, description, create_at)
VALUES ('Задача1', 'Проверочная задача 1', NOW());