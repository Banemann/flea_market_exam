-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: mysql
-- Generation Time: May 01, 2025 at 01:39 PM
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
  `image_pk` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `image_user_fk` varchar(32) NOT NULL,
  `image_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `items`
--

CREATE TABLE `items` (
  `item_pk` char(32) NOT NULL,
  `item_name` varchar(50) NOT NULL,
  `item_address` varchar(100) NOT NULL,
  `item_image` varchar(50) NOT NULL,
  `item_price` smallint UNSIGNED NOT NULL,
  `item_lon` varchar(50) NOT NULL,
  `item_lat` varchar(50) NOT NULL,
  `item_created_at` bigint UNSIGNED NOT NULL,
  `item_updated_at` bigint UNSIGNED NOT NULL,
  `Item_deleted_at` bigint UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `items`
--

INSERT INTO `items` (`item_pk`, `item_name`, `item_address`, `item_image`, `item_price`, `item_lon`, `item_lat`, `item_created_at`, `item_updated_at`, `Item_deleted_at`) VALUES
('193e055791ed4fa5a6f24d0ea7422a89', 'Tivoli Gardens', '', '2.jpg', 220, '12.5673', '55.6731', 2, 0, 0),
('56f9d2171b2646f7a077a6ee4a0ce3c9', 'The Little Mermaid Statue', '', '3.jpg', 50, '12.6030', '55.6910', 3, 0, 0),
('a9689643e38d47bc95f427902e9a1de3', 'Caspers shop', 'Richard Mortensens Vej 1', '6.webp', 50, '90.86452', '24.63822', 1745765513, 0, 0),
('b8f0c4a9fa0d4d1c8c38a1d8986e9c7d', 'Nyhavn (Harbor)', '', '1.jpg', 100, '12.5903', '55.6763', 1, 0, 0),
('cf9e4a6d71ea45cba17078df4d7b2516', 'Rosenborg Castle', '', '5.jpg', 500, '12.5844', '55.6838', 5, 0, 0),
('f08b6d7c45ff46a0a95cd13b56ab5676', 'Amalienborg Palace', '', '4.jpg', 200, '12.5917', '55.6759', 4, 0, 0);

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
  `user_deleted_at` bigint UNSIGNED NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_pk`, `user_username`, `user_name`, `user_last_name`, `user_email`, `user_password`, `user_verification_key`, `user_verified_at`, `user_created_at`, `user_updated_at`, `user_blocked_at`, `user_deleted_at`) VALUES
('0c74e53d3afe460b8a02f2ef9b5047f7', 'Emil2', 'Emil2', 'Emil2', 'lindehojpizza@gmail.com', 'scrypt:32768:8:1$8cIOTnylynjo88wa$f06dc3b97443bb8b2a6ee9359047dea821d8226d3ccf77275e20240769e445df4076ecf995c54542d5ee80acd428353384ceb4b0815496799a3c06252ff25e2b', NULL, 1745928607, 1745928600, 0, 0, 0),
('2e561df506cb460b927438f9070ff3f1', '111', 'dd', '', 'd@d.com', '', NULL, 0, 0, 0, 0, 0),
('3d7ff97dce6a4a01b21b53a5b3067d6d', '222', 'cc', '', 'c@c.com', '', NULL, 0, 0, 0, 0, 0),
('47c9425d30b84789b789d1ae69fe7ab3', '333', 'ee', '', 'e@e.com', '', NULL, 0, 0, 0, 0, 0),
('9e5a4d736dce48cc9ed9b307c5a9756b', 'Emil', 'Emil', 'Emil', 'emil@emil.com', 'scrypt:32768:8:1$R2X5dLw7Bv8702oV$bb4df70854ef6364128b39ebc42db047c6bf5991fe1071987b8ce691682760eb0f74fce716ad9a6012471a715c2b346415642c9e3d94aeb6b53d373229155bd2', '673f77af03b842a895c64dd2451f1a4b', 0, 1745928555, 0, 0, 0),
('af12f713a8ff4b079b9564dfad0cc6d7', '444', 'ff', '', 'f@f.com', '', NULL, 0, 0, 0, 0, 0),
('b6e4a3f3192d46fcb2b7c927576e6f77', '555', 'bb', '', 'b@b.com', '', NULL, 0, 0, 0, 0, 0),
('bf3d1b6e5189471a9e61713b6b644970', 'johnman', 'john', 'man', 'johnman@gmail.com', 'scrypt:32768:8:1$PUCvCrSVJyOVjdIT$9b62adcaae4d65bfe5e8e20507a5e199227f329a38bf45422217a17fcd3564cbcf903d21afe6ebd5827a60d7cd59203c253cd9f46b338b57d86117333f41fac0', NULL, 0, 1745927483, 0, 0, 0),
('d4fd565c713c4ba19700965d6a536700', 'casp2783', 'Casper', 'Banemann', 'casperbanemann@gmail.com', 'scrypt:32768:8:1$zDjz6l85YtoNlM1a$0a9c48d8a8992d8421bf7e736b3fff45584a5db8660c08a10265d2b24de5b5934a1d2ee2e4415a3b37302830587c52c455c1f261b71fff5c9a0059cb51a9a022', NULL, 1746059204, 1746059179, 0, 0, 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `images`
--
ALTER TABLE `images`
  ADD PRIMARY KEY (`image_pk`);

--
-- Indexes for table `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`item_pk`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_pk`),
  ADD UNIQUE KEY `user_email` (`user_email`),
  ADD UNIQUE KEY `user_username` (`user_username`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
