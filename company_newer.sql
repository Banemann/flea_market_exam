-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: mysql
-- Generation Time: May 24, 2025 at 01:08 PM
-- Server version: 9.3.0
-- PHP Version: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `company`
--

-- --------------------------------------------------------

--
-- Table structure for table `images`
--

CREATE TABLE `images` (
  `image_pk` varchar(255) NOT NULL,
  `image_item_fk` varchar(255) NOT NULL,
  `image_name` varchar(255) NOT NULL,
  `image_created_at` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `items`
--

CREATE TABLE `items` (
  `item_pk` char(32) NOT NULL,
  `item_user_fk` char(32) DEFAULT NULL,
  `item_name` varchar(50) NOT NULL,
  `item_address` varchar(100) NOT NULL,
  `item_image` varchar(50) NOT NULL,
  `item_price` smallint UNSIGNED NOT NULL,
  `item_lon` varchar(50) NOT NULL,
  `item_lat` varchar(50) NOT NULL,
  `item_created_at` bigint UNSIGNED NOT NULL,
  `item_updated_at` bigint UNSIGNED NOT NULL,
  `item_deleted_at` bigint UNSIGNED NOT NULL,
  `item_blocked_at` bigint UNSIGNED NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `items`
--

INSERT INTO `items` (`item_pk`, `item_user_fk`, `item_name`, `item_address`, `item_image`, `item_price`, `item_lon`, `item_lat`, `item_created_at`, `item_updated_at`, `item_deleted_at`, `item_blocked_at`) VALUES
('53c3db7120bd4be0bfad62c185237014', 'f490d2b887914af78d22f21907177912', 'Nørrebro Flea', 'Nørregade 51', '4be2ae7115cc44fea01b17f084e9fb6f.jpg', 90, '80.86452', '14.63822', 1746385792, 0, 0, 0),
('94b884e783204fa7ab3b6c5acee74ea2', 'af12f713a8ff4b079b9564dfad0cc6d7', 'Caspers shop', 'Richard Mortensens Vej 1', '8ca016bee0854caeb5f1d509b2411495.jpg', 50, '12.5683', '55.6761', 1746390535, 1747920758, 0, 0),
('bb7491ac6c2046c39e8b495ac399df3d', 'af12f713a8ff4b079b9564dfad0cc6d7', 'Caspers shop12', 'Richard Mortensens Vej 15', '8f9c4be9c86b4aebbe6be34eab79ece9.jpg', 50, '90.86452', '24.63822', 1746447001, 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_pk` char(32) NOT NULL,
  `user_username` varchar(30) NOT NULL,
  `user_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `user_last_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `user_email` varchar(100) NOT NULL,
  `user_password` varchar(255) NOT NULL,
  `user_verification_key` char(32) DEFAULT NULL,
  `user_verified_at` bigint UNSIGNED NOT NULL DEFAULT '0',
  `user_created_at` bigint UNSIGNED NOT NULL,
  `user_updated_at` bigint UNSIGNED NOT NULL DEFAULT '0',
  `user_blocked_at` bigint UNSIGNED NOT NULL DEFAULT '0',
  `user_deleted_at` bigint UNSIGNED NOT NULL DEFAULT '0',
  `user_is_admin` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_pk`, `user_username`, `user_name`, `user_last_name`, `user_email`, `user_password`, `user_verification_key`, `user_verified_at`, `user_created_at`, `user_updated_at`, `user_blocked_at`, `user_deleted_at`, `user_is_admin`) VALUES
('af12f713a8ff4b079b9564dfad0cc6d7', 'admin', 'admin', 'admin', 'admin', 'scrypt:32768:8:1$X9CnDA61WqTCXIJl$35da40c4084ffeae93c5544a316d7fe99b6ebca25a821060df284f754ae9a144e0b30101cb8654712313d441b5d3ccfb9f6560606be687d1eea5705ffcaefc18', NULL, 1746381070, 1746381055, 0, 0, 0, 1),
('f490d2b887914af78d22f21907177912', 'casp2783', 'Casper', 'Banemann', 'anqlzxx@gmail.com', 'scrypt:32768:8:1$QOICi6l4SMuHgGdR$6ce75bef777b0d5e68f82bd135f616b013624977fcaac06da75a7f153eea6ffbf198d19d4ae62357a54f29592ff4610a93a62b520fd447945e00856b11c3098f', NULL, 1746385721, 1746385687, 0, 0, 0, 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `images`
--
ALTER TABLE `images`
  ADD PRIMARY KEY (`image_pk`),
  ADD KEY `image_item_fk` (`image_item_fk`);

--
-- Indexes for table `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`item_pk`),
  ADD UNIQUE KEY `item_name` (`item_name`),
  ADD UNIQUE KEY `item_address` (`item_address`),
  ADD KEY `item_user_fk` (`item_user_fk`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_pk`),
  ADD UNIQUE KEY `user_email` (`user_email`),
  ADD UNIQUE KEY `user_username` (`user_username`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `images`
--
ALTER TABLE `images`
  ADD CONSTRAINT `images_ibfk_1` FOREIGN KEY (`image_item_fk`) REFERENCES `items` (`item_pk`);

--
-- Constraints for table `items`
--
ALTER TABLE `items`
  ADD CONSTRAINT `items_ibfk_1` FOREIGN KEY (`item_user_fk`) REFERENCES `users` (`user_pk`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
