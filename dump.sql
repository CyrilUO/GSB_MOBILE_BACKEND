-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Base de données : `gsb_mobile`
--
CREATE DATABASE IF NOT EXISTS `gsb_mobile` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci

USE `gsb_mobile`;

-- Désactivation des contraintes pour éviter les erreurs de dépendance
SET FOREIGN_KEY_CHECKS=0;

-- Table `categories`
DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
                              `id` int NOT NULL AUTO_INCREMENT,
                              `name` varchar(100) NOT NULL,
                              PRIMARY KEY (`id`),
                              UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
;

INSERT INTO `categories` VALUES
                             (1,'Antibiotiques'),
                             (2,'Antalgiques'),
                             (3,'Vitamines'),
                             (4,'Allergies'),
                             (5,'Cardiologie');

-- Table `products`
DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` (
                            `id` int NOT NULL AUTO_INCREMENT,
                            `name` varchar(255) NOT NULL,
                            `description` text NOT NULL,
                            `price` decimal(10,2) NOT NULL,
                            `category_id` int DEFAULT NULL,
                            `image_url` varchar(255) DEFAULT NULL,
                            `manufacturer` varchar(255) DEFAULT NULL,
                            `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
                            PRIMARY KEY (`id`),
                            KEY `category_id` (`category_id`),
                            CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
;

INSERT INTO `products` VALUES
                           (1,'Amoxicilline 500mg','Un antibiotique efficace contre les infections bactériennes.',12.50,1,'https://example.com/images/amoxicilline.jpg','Laboratoire X','2025-03-02 22:43:32'),
                           (2,'Paracétamol 1000mg','Un antalgique utilisé pour soulager la douleur et la fièvre.',5.75,2,'https://example.com/images/paracetamol.jpg','Laboratoire Y','2025-03-02 22:43:32'),
                           (3,'Vitamine C 500mg','Complément alimentaire pour renforcer le système immunitaire.',8.99,3,'https://example.com/images/vitamine_c.jpg','Laboratoire Z','2025-03-02 22:43:32');

-- Table `users`
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
                         `id` int NOT NULL AUTO_INCREMENT,
                         `username` varchar(55) NOT NULL,
                         `email` varchar(100) NOT NULL,
                         `password` varchar(255) NOT NULL,
                         `role` enum('admin','editor','user') DEFAULT 'user',
                         `profile_picture_url` varchar(255) DEFAULT NULL,
                         `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
                         PRIMARY KEY (`id`),
                         UNIQUE KEY `username` (`username`),
                         UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
;

INSERT INTO `users` VALUES
                        (3,'user1','user1@example.com','hashed_password_3','user','https://example.com/images/user1.jpg','2025-03-02 22:42:57'),
                        (4,'user2','user2@example.com','hashed_password_4','user',NULL,'2025-03-02 22:42:57');

-- Table `articles`
DROP TABLE IF EXISTS `articles`;
CREATE TABLE `articles` (
                            `id` int NOT NULL AUTO_INCREMENT,
                            `title` varchar(255) NOT NULL,
                            `content` text NOT NULL,
                            `product_id` int NOT NULL,
                            `author_id` int NOT NULL,
                            `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
                            PRIMARY KEY (`id`),
                            KEY `product_id` (`product_id`),
                            KEY `author_id` (`author_id`),
                            CONSTRAINT `articles_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE,
                            CONSTRAINT `articles_ibfk_2` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
;

-- Table `comments`
DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
                            `id` int NOT NULL AUTO_INCREMENT,
                            `user_id` int NOT NULL,
                            `article_id` int DEFAULT NULL,
                            `product_id` int DEFAULT NULL,
                            `content` text NOT NULL,
                            `rating` int DEFAULT NULL CHECK (`rating` BETWEEN 1 AND 5),
                            `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
                            PRIMARY KEY (`id`),
                            KEY `user_id` (`user_id`),
                            KEY `article_id` (`article_id`),
                            KEY `product_id` (`product_id`),
                            CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
                            CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`article_id`) REFERENCES `articles` (`id`) ON DELETE CASCADE,
                            CONSTRAINT `comments_ibfk_3` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
;

INSERT INTO `comments` VALUES
                           (2,3,NULL,1,'Très efficace contre les infections. Je recommande !',5,'2025-03-02 22:44:00'),
                           (3,4,NULL,2,'Soulage bien la douleur mais attention au surdosage.',4,'2025-03-02 22:44:00');

-- Réactivation des contraintes
SET FOREIGN_KEY_CHECKS=1;
