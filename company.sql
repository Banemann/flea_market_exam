-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: mysql
-- Generation Time: Apr 29, 2025 at 11:32 AM
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
  `user_created_at` bigint UNSIGNED NOT NULL,
  `user_updated_at` bigint UNSIGNED NOT NULL DEFAULT '0',
  `user_deleted_at` bigint UNSIGNED NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_pk`, `user_username`, `user_name`, `user_last_name`, `user_email`, `user_password`, `user_verification_key`, `user_created_at`, `user_updated_at`, `user_deleted_at`) VALUES
('2c8a4146351841c2951c35cfb362b29f', 'casp2783', 'Casper', 'Banemann', 'casperbanemann@gmail.com', 'scrypt:32768:8:1$kfVHzynSVGvqPAhr$75eef06dff972a505648a71dcfedca97131f5132e773a430ce928b2c97023f607ce8415656748b8d7e470da241653322bc9dd604304079727745b37ae7d6efad', NULL, 1745762610, 0, 0),
('2e561df506cb460b927438f9070ff3f1', '', 'dd', '', 'd@d.com', '', NULL, 0, 0, 0),
('3d7ff97dce6a4a01b21b53a5b3067d6d', '', 'cc', '', 'c@c.com', '', NULL, 0, 0, 0),
('47c9425d30b84789b789d1ae69fe7ab3', '', 'ee', '', 'e@e.com', '', NULL, 0, 0, 0),
('af12f713a8ff4b079b9564dfad0cc6d7', '', 'ff', '', 'f@f.com', '', NULL, 0, 0, 0),
('b6e4a3f3192d46fcb2b7c927576e6f77', '', 'bb', '', 'b@b.com', '', NULL, 0, 0, 0),
('ccad60125be84df5aca4df3fa005d628', '', 'aa', '', 'a@a.com', '', NULL, 0, 0, 1742382471);

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
  ADD UNIQUE KEY `user_email` (`user_email`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
