CREATE DATABASE lista_telefonica;
USE lista_telefonica;


CREATE TABLE pessoa (
	id_pessoa INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    email VARCHAR(200) NOT NULL
);

CREATE TABLE setor (
	id_setor INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    email VARCHAR(200) NOT NULL,
    ramal VARCHAR(10) NOT NULL,
    text_alter VARCHAR(150)
);

CREATE TABLE pessoa_setor (
	id_pessoa INT NOT NULL,
    id_setor INT NOT NULL,
    FOREIGN KEY (id_pessoa) REFERENCES pessoa (id_pessoa),
	FOREIGN KEY (id_setor) REFERENCES setor (id_setor),
    PRIMARY KEY(id_pessoa, id_setor)
);

CREATE TABLE usuario (
	id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    email VARCHAR(200) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    status_usuario VARCHAR(10) NOT NULL,
    nivel_acesso VARCHAR(20) NOT NULL
);