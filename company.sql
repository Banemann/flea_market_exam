-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: mysql
-- Generation Time: Jun 09, 2025 at 02:26 PM
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

--
-- Dumping data for table `images`
--

INSERT INTO `images` (`image_pk`, `image_item_fk`, `image_name`, `image_created_at`) VALUES
('65dbc1d2ae624112a27f7c7eeae3b8d8', 'c00ec476afd54f75b2e4da8d187f582c', 'ac3e930f7abd4766831aadb52193523e.jpg', 1749478704),
('8e70cb2ea1db435ca531efc24b519083', 'c00ec476afd54f75b2e4da8d187f582c', 'aad6d35edbfa461e9df3df192020e396.jpg', 1749478704);

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
('28bc967e6bda4200a26c6f68bb7fe83a', '9c5476dd65da4e8b83aa46311876d72f', 'CBS', 'Jydevej 12', '8f9c4be9c86b4aebbe6be34eab79ece9.png', 34, '12.5211', '55.6781', 1746447001, 0, 0, 0),
('28bc967e6bda4200a26c6f68bb7fe83e', '9c5476dd65da4e8b83aa46311876d72f', 'Top Market', 'Jørgenvej 1', 'e462b4da12844149b09a365f0f56d85e.jpg', 37, '12.5683', '55.6761', 1749299424, 1749300474, 0, 0),
('53c3db7120bd4be0bfad62c185237014', 'f490d2b887914af78d22f21907177912', 'Nørrebro Flea', 'Nørregade 51', '4be2ae7115cc44fea01b17f084e9fb6f.png', 90, '12.4683', '55.6761', 1746385792, 1749300442, 0, 0),
('94b884e783204fa7ab3b6c5acee74ea2', 'af12f713a8ff4b079b9564dfad0cc6d7', 'KEA shop', 'Richard Sigurds Vej 1', '8ca016bee0854caeb5f1d509b2411495.png', 50, '12.5899', '55.6595', 1746390535, 1749300412, 0, 0),
('bb7491ac6c2046c39e8b495ac399df3d', 'af12f713a8ff4b079b9564dfad0cc6d7', 'Caspers shop12', 'Richard Mortensens Vej 15', '8f9c4be9c86b4aebbe6be34eab79ece9.png', 50, '90.86452', '24.63822', 1746447001, 0, 0, 0),
('c00ec476afd54f75b2e4da8d187f582c', 'f873700036be46e8b954a92521bdff84', 'Testmarket', 'Testvej 54', '0c07a1bd425848008c896f9381d46813.jpg', 410, '12.5669', '55.6749', 1749478704, 1749478849, 0, 0);

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
('47eaf45d8bd74222ae90fc24a0944943', 'asdada', 'asdasd', 'asdasdda', 'casperbaneasddmann@gmail.com', 'scrypt:32768:8:1$DymkE5tfI1VrJo0E$11112b89d4a25aeea3bc7b2dccb584915bd829a198f5e72d9ef1645a2407815b89f6708a58ea6ede24f3d3b06767b803c9f3c15ecab92afdc4e8bd7b067cffae', '018f840b46f34d44bba69d696b905d6b', 0, 1749136069, 0, 0, 0, 0),
('68e1d17cb8a04b41bad860e3bfbe202d', 'casp27832w', 'asdasdasdasd', 'dadasdasdasdas', 'a@gmil.comasd', 'scrypt:32768:8:1$wKXEhAcPaN1PvsfV$af530caa64133b423a3bf7ebf41c642998d885fccfc6f08ad1f945361ee202024a772ec98e0b60d039149c93bfc4db2049f57b0e14596759452281e834189c33', '7151136fbf254b06912df989329f3e4c', 0, 1749136114, 0, 0, 0, 0),
('9c5476dd65da4e8b83aa46311876d72f', 'casperb', 'casperb', 'bbb', 'casperbanemann@gmail.com11', 'scrypt:32768:8:1$BoTDTmDrLXikhrLP$80b691394c1f7e5295c9f639393e8cdde973160cd5e5c3bfcc231c32b73714cd4078366cdbe219a0f9e32f8e67a7a86a429d760b4c135e221d10c82998665fe0', NULL, 1749298926, 1749298879, 0, 0, 0, 0),
('af12f713a8ff4b079b9564dfad0cc6d7', 'admin', 'admin', 'admin', 'admin', 'scrypt:32768:8:1$X9CnDA61WqTCXIJl$35da40c4084ffeae93c5544a316d7fe99b6ebca25a821060df284f754ae9a144e0b30101cb8654712313d441b5d3ccfb9f6560606be687d1eea5705ffcaefc18', NULL, 1746381070, 1746381055, 0, 0, 0, 1),
('b05aca5c850744c49e4f57f0777c01a2', 'testuser', 'Casper', 'Banemann', 'casperbanemann@gmail.com645', 'scrypt:32768:8:1$8DNSEhX0Jsg5mEJP$fb60b5f9fbf610d67654a4ae877a49cfc715e05444ff461e67c51d81e303624b5da0b1bb56f20c3539b656d7eee76ca5dc0fd018f64136c6e733cd20b127fb26', 'f9a9180897364bf0b957bf48adef94bf', 0, 1749475638, 1749477260, 0, 0, 0),
('d0f67f43c69a4d4a8ddd2dc88256faeb', 'casp33327832w', 'asdasdasdasd', 'dadasdasdasdas', 'a333@gmil.com', 'scrypt:32768:8:1$eXtellY2eKMyGOUv$b10419522cd41d3142a6840c30d399d4badd2b074c81e65094fc8274846195a699fbfda4aeffc531bec8f92f38fc3c117a019b9a5c2d46b7b00c1b37883a447f', '66015b9ba43446bdac51a25a4053cc35', 0, 1749136211, 0, 0, 0, 0),
('eb92992ddcf54892a3673bc1082ae95a', 'asdsada', 'asdasd', 'asdasd', 'casper3333banemann@gmail.com', 'scrypt:32768:8:1$Uf5xScdXxFXcme4M$56dc7adca73edeb78f5cd733a1454d7bdf08ce4263f4a4c5487070a9237053498f06abb2635e3f85bc0312d16bc4be471db42a02ee6364daedc28d2faa68831b', NULL, 1748372207, 1748372179, 0, 0, 0, 0),
('f490d2b887914af78d22f21907177912', 'casp2783', 'Casper', 'Banemann', 'anqlzx213123x@gmail.com', 'scrypt:32768:8:1$Ag8CB16Ppie7vxMv$1a223955e66021296135667326180a00c04614e446a5c0e3ee5dda9851ab045dd6fbb5b629781a1ae57c605ae691b8a88beedba604d49938dd5ade98d8833ca8', NULL, 1746385721, 1746385687, 1748376335, 0, 0, 0),
('f873700036be46e8b954a92521bdff84', 'tester', 'tester', 'tester', 'casperbanemann@gmail.com', 'scrypt:32768:8:1$8B7Kx8qx0Zv9F2BW$df9094b12721b2ba5dfb04e3fb861a9308b404521ab726c3497357457dd0a94301957869b5015f42be7cc03542dd2cdc005d3bc33cd59e0acfdc2e769e32e13d', NULL, 1749478645, 1749478635, 0, 0, 0, 0);

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
