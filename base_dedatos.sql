CREATE DATABASE IF NOT EXISTS joan_8;

USE joan_8;

CREATE TABLE IF NOT EXISTS users(
	id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    fecha_registro datetime default now(),
    ultimo_login datetime 
);

CREATE TABLE IF NOT EXISTS favoritos(
	id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    user_id INT NOT NULL,
    imagen TEXT,
    nombre TEXT,
    genero TEXT,
    
	foreign key (user_id) references users(id)
		ON DELETE CASCADE
        ON UPDATE CASCADE
    
)