-- Script SQL para MySQL / MariaDB (phpMyAdmin, XAMPP, etc.)
-- Opcional: la aplicación crea las tablas sola con db.create_all()

CREATE DATABASE IF NOT EXISTS bd_anuncios
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE bd_anuncios;

CREATE TABLE IF NOT EXISTS usuarios (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  nombre        VARCHAR(100) NOT NULL,
  email         VARCHAR(120) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS categorias (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  nombre      VARCHAR(80) NOT NULL UNIQUE,
  descripcion VARCHAR(255)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS anuncios (
  id           INT AUTO_INCREMENT PRIMARY KEY,
  titulo       VARCHAR(150) NOT NULL,
  contenido    TEXT NOT NULL,
  fecha        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  usuario_id   INT NOT NULL,
  categoria_id INT NOT NULL,
  CONSTRAINT fk_anuncio_usuario   FOREIGN KEY (usuario_id)   REFERENCES usuarios(id),
  CONSTRAINT fk_anuncio_categoria FOREIGN KEY (categoria_id) REFERENCES categorias(id)
) ENGINE=InnoDB;

-- Relaciones:
--   usuarios 1 ---- N anuncios
--   categorias 1 -- N anuncios
