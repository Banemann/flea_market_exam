-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: mysql
-- Generation Time: May 04, 2025 at 05:52 PM
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
  `item_deleted_at` bigint UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `items`
--

INSERT INTO `items` (`item_pk`, `item_user_fk`, `item_name`, `item_address`, `item_image`, `item_price`, `item_lon`, `item_lat`, `item_created_at`, `item_updated_at`, `item_deleted_at`) VALUES
('193e055791ed4fa5a6f24d0ea7422a89', NULL, 'Tivoli Gardens', '1111', '2.jpg', 220, '12.5673', '55.6731', 2, 0, 0),
('56f9d2171b2646f7a077a6ee4a0ce3c9', NULL, 'The Little Mermaid Statue', '112222', '3.jpg', 50, '12.6030', '55.6910', 3, 0, 0),
('b8f0c4a9fa0d4d1c8c38a1d8986e9c7d', NULL, 'Nyhavn (Harbor)', '22323', '1.jpg', 100, '12.5903', '55.6763', 1, 0, 0),
('cf9e4a6d71ea45cba17078df4d7b2516', NULL, 'Rosenborg Castle', '3333', '5.jpg', 500, '12.5844', '55.6838', 5, 0, 0),
('f08b6d7c45ff46a0a95cd13b56ab5676', NULL, 'Amalienborg Palace', '444444', '4.jpg', 200, '12.5917', '55.6759', 4, 0, 0);

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
('2e561df506cb460b927438f9070ff3f1', '111', 'dd', '', 'd@d.com', '', NULL, 0, 0, 0, 0, 0, 0),
('3d7ff97dce6a4a01b21b53a5b3067d6d', '222', 'cc', '', 'c@c.com', '', NULL, 0, 0, 0, 0, 0, 0),
('47c9425d30b84789b789d1ae69fe7ab3', '333', 'ee', '', 'e@e.com', '', NULL, 0, 0, 0, 0, 0, 0),
('6c99c026fb2847e2ba0a67ec1d747f4b', 'admin', 'admin', 'admin', 'casperbanemann@gmail.com', 'scrypt:32768:8:1$X9CnDA61WqTCXIJl$35da40c4084ffeae93c5544a316d7fe99b6ebca25a821060df284f754ae9a144e0b30101cb8654712313d441b5d3ccfb9f6560606be687d1eea5705ffcaefc18', NULL, 1746381070, 1746381055, 0, 0, 0, 1),
('9e5a4d736dce48cc9ed9b307c5a9756b', 'Emil', 'Emil', 'Emil', 'emil@emil.com', 'scrypt:32768:8:1$R2X5dLw7Bv8702oV$bb4df70854ef6364128b39ebc42db047c6bf5991fe1071987b8ce691682760eb0f74fce716ad9a6012471a715c2b346415642c9e3d94aeb6b53d373229155bd2', '673f77af03b842a895c64dd2451f1a4b', 0, 1745928555, 0, 0, 0, 0),
('af12f713a8ff4b079b9564dfad0cc6d7', '444', 'ff', '', 'f@f.com', '', NULL, 0, 0, 0, 0, 0, 0),
('b6e4a3f3192d46fcb2b7c927576e6f77', '555', 'bb', '', 'b@b.com', '', NULL, 0, 0, 0, 0, 0, 0);

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
