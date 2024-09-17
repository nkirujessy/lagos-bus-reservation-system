-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Aug 07, 2023 at 01:53 AM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `lbrs`
--

-- --------------------------------------------------------

--
-- Table structure for table `bus`
--

CREATE TABLE `bus` (
  `id` varchar(36) NOT NULL,
  `name` varchar(225) NOT NULL,
  `description` varchar(225) NOT NULL,
  `image` varchar(225) DEFAULT NULL,
  `adult` int NOT NULL,
  `children` int NOT NULL,
  `max_occupancy` int NOT NULL,
  `status` int NOT NULL,
  `driverId` varchar(225) NOT NULL,
  `created` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `bus`
--

INSERT INTO `bus` (`id`, `name`, `description`, `image`, `adult`, `children`, `max_occupancy`, `status`, `driverId`, `created`) VALUES
('9701ae29-2274-4de2-af3a-2ea52a930378', 'BUS001', 'This works too', NULL, 25, 5, 30, 1, '32a102f4-389a-4dc6-ba40-f42af33d9cr6', '2023-08-06 16:51:41');

-- --------------------------------------------------------

--
-- Table structure for table `busstop`
--

CREATE TABLE `busstop` (
  `id` varchar(36) NOT NULL,
  `name` varchar(225) NOT NULL,
  `description` varchar(225) NOT NULL,
  `routeId` varchar(255) NOT NULL,
  `latitude` varchar(255) NOT NULL,
  `longitude` varchar(255) NOT NULL,
  `landmark` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `zipcode` varchar(255) NOT NULL,
  `status` int NOT NULL,
  `created` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `busstop`
--

INSERT INTO `busstop` (`id`, `name`, `description`, `routeId`, `latitude`, `longitude`, `landmark`, `address`, `zipcode`, `status`, `created`) VALUES
('552dd284-587a-4d9c-a79c-e03897eede02', 'BUS STOP 001', 'THIS IS BUS STOP 001', '9ce4d048-2a1a-4442-b072-4dfed59a2ba5', '4747835774', '477475577', 'City college before commissioners house', 'No 6 Chukwuma Close, 4', '961105', 1, '2023-08-07 02:13:10');

-- --------------------------------------------------------

--
-- Table structure for table `location`
--

CREATE TABLE `location` (
  `id` varchar(36) NOT NULL,
  `name` varchar(225) NOT NULL,
  `status` int NOT NULL,
  `created` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `location`
--

INSERT INTO `location` (`id`, `name`, `status`, `created`) VALUES
('19b31cb0-4d9d-4640-ba55-40da5db63933', 'Ikorodu', 1, '2023-07-23 19:41:37'),
('19f3d5db-36bc-49c6-822a-495df1ae2657', 'Mushin', 1, '2023-07-23 19:41:25'),
('20726d50-6d9e-4523-952b-08524cdb3de6', 'Badagry', 1, '2023-07-23 19:42:17'),
('2df859b0-3e38-4bab-901f-1be88ae74796', 'Agege', 1, '2023-07-23 19:41:53'),
('4b5f4426-4c85-4410-bba4-f68196369ec7', 'Somolu', 1, '2023-07-23 19:42:04'),
('54c12f28-f7bd-4f51-a9e4-1ff58b1ea977', 'Surulere', 1, '2023-07-23 19:41:39'),
('59e1920b-ecad-4d47-8d02-d3b177f49f04', 'Kosofe', 1, '2023-07-23 19:41:23'),
('71cec5fd-7630-4328-8b97-b34407780978', 'Ikeja', 1, '2023-07-23 19:42:12'),
('73dc80fc-102a-49be-9a2f-12d6e377118a', 'Eti-Osa', 1, '2023-07-23 19:42:14'),
('780537fd-f4a3-4623-8452-66e966a4a83b', 'Ifako-Ijaiye', 1, '2023-07-23 19:42:00'),
('85cf526f-e566-4208-8614-1826a3f41f7d', 'Epe', 1, '2023-07-23 19:42:23'),
('a3d9fdb7-17bf-47e1-b199-e17148f275c1', 'Ibeju-Lekki', 1, '2023-07-23 19:42:27'),
('bd4338f0-cec0-491e-8055-6d7dad490c43', 'Lagos Island', 1, '2023-07-23 19:42:21'),
('c7242fef-203d-4412-871e-b39823f21b60', 'Alimosho', 1, '2023-07-23 19:41:06'),
('c9d68469-969b-4ee2-8c8f-5ddb3deeae1a', 'Oshodi-Isolo', 1, '2023-07-23 19:41:32'),
('dc177e44-6793-4af9-9ec6-bcb41fbd7a84', 'Ajeromi-Ifelodun', 1, '2023-07-23 19:41:15'),
('e19f25b8-66eb-42e3-a7c8-c37705c503b1', 'Ojo', 1, '2023-07-23 19:41:34'),
('e3eabd57-0a83-415d-a914-5f21d0d7aed4', 'Apapa', 1, '2023-07-23 19:42:19'),
('f27d5fd4-5a0a-4c15-9168-470d0aef731f', 'Lagos Mainland', 1, '2023-07-23 19:42:10'),
('f3b974b1-a8fd-4723-bbeb-9c8f90a689e1', 'Amuwo-Odofin', 1, '2023-07-23 19:42:08');

-- --------------------------------------------------------

--
-- Table structure for table `reservation`
--

CREATE TABLE `reservation` (
  `id` varchar(36) NOT NULL,
  `userId` varchar(225) NOT NULL,
  `ticketId` varchar(225) NOT NULL,
  `reservation_number` varchar(225) NOT NULL,
  `adult` int NOT NULL,
  `children` int NOT NULL,
  `status` int NOT NULL,
  `created` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `reservation`
--

INSERT INTO `reservation` (`id`, `userId`, `ticketId`, `reservation_number`, `adult`, `children`, `status`, `created`) VALUES
('5268b07a-3588-4054-bc4d-3a57ce2db780', '48a102f4-389a-4dc6-ba40-f42af33d9cr4', 'a954e276-812d-4ebf-a607-6c190b912f2d', 'KLPJ5UTF', 1, 0, 1, '2023-08-06 17:58:42'),
('74c23fe8-88c3-472f-9f60-4814d60eea4b', '48a102f4-389a-4dc6-ba40-f42af33d9cr4', 'a954e276-812d-4ebf-a607-6c190b912f2d', 'JBSOBU6X', 1, 0, 1, '2023-08-06 17:59:37');

-- --------------------------------------------------------

--
-- Table structure for table `routes`
--

CREATE TABLE `routes` (
  `id` varchar(36) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `start_routeId` varchar(255) NOT NULL,
  `end_routeId` varchar(255) NOT NULL,
  `status` int NOT NULL,
  `created` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `routes`
--

INSERT INTO `routes` (`id`, `name`, `description`, `start_routeId`, `end_routeId`, `status`, `created`) VALUES
('9ce4d048-2a1a-4442-b072-4dfed59a2ba5', 'Route 001', 'This is route 001', 'c7242fef-203d-4412-871e-b39823f21b60', '20726d50-6d9e-4523-952b-08524cdb3de6', 1, '2023-08-06 16:54:12');

-- --------------------------------------------------------

--
-- Table structure for table `settings`
--

CREATE TABLE `settings` (
  `id` varchar(36) NOT NULL,
  `appname` varchar(225) NOT NULL,
  `currency` varchar(225) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `id` varchar(36) NOT NULL,
  `name` varchar(225) NOT NULL,
  `description` varchar(225) NOT NULL,
  `fee` int NOT NULL,
  `ticket_number` varchar(225) NOT NULL,
  `routeId` varchar(225) NOT NULL,
  `busId` varchar(225) NOT NULL,
  `driverId` varchar(225) NOT NULL,
  `available` int NOT NULL,
  `availability_date` date NOT NULL,
  `arrival_datetime` datetime NOT NULL,
  `departure_datetime` datetime NOT NULL,
  `status` int NOT NULL,
  `created` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`id`, `name`, `description`, `fee`, `ticket_number`, `routeId`, `busId`, `driverId`, `available`, `availability_date`, `arrival_datetime`, `departure_datetime`, `status`, `created`) VALUES
('a954e276-812d-4ebf-a607-6c190b912f2d', 'Ticket 001', 'This is ticket 001', 1000, '0O9DUGRT', '9ce4d048-2a1a-4442-b072-4dfed59a2ba5', '9701ae29-2274-4de2-af3a-2ea52a930378', '32a102f4-389a-4dc6-ba40-f42af33d9cr6', 1, '2023-08-07', '2023-08-07 10:30:00', '2023-08-07 09:30:00', 1, '2023-08-06 17:06:38');

-- --------------------------------------------------------

--
-- Table structure for table `transaction`
--

CREATE TABLE `transaction` (
  `id` varchar(36) NOT NULL,
  `reference` varchar(255) DEFAULT NULL,
  `amount` int DEFAULT NULL,
  `reservationId` varchar(225) NOT NULL,
  `userId` varchar(225) NOT NULL,
  `status` int NOT NULL,
  `created` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `transaction`
--

INSERT INTO `transaction` (`id`, `reference`, `amount`, `reservationId`, `userId`, `status`, `created`) VALUES
('b08653cc-8dfe-49f6-ac77-932636840bcb', 'e464a79b-edd0-427b-9de4-68ff56e7a606', 1000, '5268b07a-3588-4054-bc4d-3a57ce2db780', '48a102f4-389a-4dc6-ba40-f42af33d9cr4', 1, '2023-08-06 17:58:42'),
('cc5d4fbe-69d1-4448-b426-6bf3733c4fe6', '72777da6-dd61-4af5-b489-50e7617d049c', 1000, '74c23fe8-88c3-472f-9f60-4814d60eea4b', '48a102f4-389a-4dc6-ba40-f42af33d9cr4', 1, '2023-08-06 17:59:37');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` varchar(36) NOT NULL,
  `fullname` varchar(225) NOT NULL,
  `password` varchar(225) NOT NULL,
  `email` varchar(225) NOT NULL,
  `role` varchar(225) NOT NULL,
  `status` int NOT NULL,
  `created` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `fullname`, `password`, `email`, `role`, `status`, `created`) VALUES
('32a102f4-389a-4dc6-ba40-f42af33d9cr6', 'Driver One', 'pbkdf2:sha256:600000$371n3qkoRzMSrOi0$1096b564153cfdca4db8f5273856e2b359e12ebda69c895883b4061aeb20af79', 'driver1@gmail.com', 'driver', 1, '2023-08-04 22:05:19'),
('48a102f4-389a-4dc6-ba40-f42af33d9cc8', 'Mcdavid Obioha', 'pbkdf2:sha256:600000$371n3qkoRzMSrOi0$1096b564153cfdca4db8f5273856e2b359e12ebda69c895883b4061aeb20af79', 'mcdave92@gmail.com', 'user', 1, '2023-08-04 22:05:19'),
('48a102f4-389a-4dc6-ba40-f42af33d9cr4', 'Super Admin', 'pbkdf2:sha256:600000$371n3qkoRzMSrOi0$1096b564153cfdca4db8f5273856e2b359e12ebda69c895883b4061aeb20af79', 'admin@gmail.com', 'admin', 1, '2023-08-04 22:05:19');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bus`
--
ALTER TABLE `bus`
  ADD PRIMARY KEY (`id`),
  ADD KEY `driverId` (`driverId`);

--
-- Indexes for table `busstop`
--
ALTER TABLE `busstop`
  ADD PRIMARY KEY (`id`),
  ADD KEY `routeId` (`routeId`);

--
-- Indexes for table `location`
--
ALTER TABLE `location`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `reservation`
--
ALTER TABLE `reservation`
  ADD PRIMARY KEY (`id`),
  ADD KEY `userId` (`userId`),
  ADD KEY `ticketId` (`ticketId`);

--
-- Indexes for table `routes`
--
ALTER TABLE `routes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `start_routeId` (`start_routeId`),
  ADD KEY `end_routeId` (`end_routeId`);

--
-- Indexes for table `settings`
--
ALTER TABLE `settings`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`id`),
  ADD KEY `routeId` (`routeId`),
  ADD KEY `busId` (`busId`),
  ADD KEY `driverId` (`driverId`);

--
-- Indexes for table `transaction`
--
ALTER TABLE `transaction`
  ADD PRIMARY KEY (`id`),
  ADD KEY `reservationId` (`reservationId`),
  ADD KEY `userId` (`userId`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bus`
--
ALTER TABLE `bus`
  ADD CONSTRAINT `bus_ibfk_1` FOREIGN KEY (`driverId`) REFERENCES `users` (`id`);

--
-- Constraints for table `busstop`
--
ALTER TABLE `busstop`
  ADD CONSTRAINT `busstop_ibfk_1` FOREIGN KEY (`routeId`) REFERENCES `routes` (`id`);

--
-- Constraints for table `reservation`
--
ALTER TABLE `reservation`
  ADD CONSTRAINT `reservation_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `reservation_ibfk_2` FOREIGN KEY (`ticketId`) REFERENCES `ticket` (`id`);

--
-- Constraints for table `routes`
--
ALTER TABLE `routes`
  ADD CONSTRAINT `routes_ibfk_1` FOREIGN KEY (`start_routeId`) REFERENCES `location` (`id`),
  ADD CONSTRAINT `routes_ibfk_2` FOREIGN KEY (`end_routeId`) REFERENCES `location` (`id`);

--
-- Constraints for table `ticket`
--
ALTER TABLE `ticket`
  ADD CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`routeId`) REFERENCES `routes` (`id`),
  ADD CONSTRAINT `ticket_ibfk_2` FOREIGN KEY (`busId`) REFERENCES `bus` (`id`),
  ADD CONSTRAINT `ticket_ibfk_3` FOREIGN KEY (`driverId`) REFERENCES `users` (`id`);

--
-- Constraints for table `transaction`
--
ALTER TABLE `transaction`
  ADD CONSTRAINT `transaction_ibfk_1` FOREIGN KEY (`reservationId`) REFERENCES `reservation` (`id`),
  ADD CONSTRAINT `transaction_ibfk_2` FOREIGN KEY (`userId`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
