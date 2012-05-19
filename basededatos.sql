CREATE DATABASE Serpiente;

GRANT ALL ON Serpiente.* TO 'conan'@'localhost' IDENTIFIED BY 'crom';
USE serpiente;
CREATE TABLE Puntos (id INT, Nombre VARCHAR(100),Puntuacion INT);


QUIT
