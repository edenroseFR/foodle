DROP DATABASE IF EXISTS `fododb`;
CREATE DATABASE `fododb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `fododb`;

CREATE TABLE `roles` (
  `role_id` int NOT NULL AUTO_INCREMENT,
  `role_name` varchar(50) NOT NULL,
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO roles (role_name)
VALUES ('indiv-donor'), ('org-donor'), ('collector');

CREATE TABLE `transport_modes` (
  `mode_id` int NOT NULL AUTO_INCREMENT,
  `mode_name` varchar(50) NOT NULL,
  PRIMARY KEY (`mode_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO transport_modes (mode_name)
VALUES ('pick-up'), ('walk-in');

CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `middle_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL UNIQUE,
  `password` varchar(300) NOT NULL,
  `phone_number` varchar(11) DEFAULT NULL,
  `org_name` varchar(100) DEFAULT NULL,
  `about` varchar(300) DEFAULT NULL,
  `street` varchar(100) NOT NULL,
  `barangay` varchar(100) NOT NULL,
  `city` varchar(100) NOT NULL,
  `image_link` varchar(200) DEFAULT NULL,
  `user_role` int NOT NULL,
  `public_profile` tinyint(1) DEFAULT 1,
  `show_donor_name` tinyint(1) DEFAULT 1,
  `notifications` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`user_id`),
  KEY `user_role` (`user_role`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`user_role`) REFERENCES `roles` (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `categories` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(50) NOT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO categories (category_name)
VALUES ('Fruit and vegetables'), ('Starchy food'), ('Dairy'), ('Protein') ,('Fat');

CREATE TABLE `donations` (
  `donation_id` int NOT NULL AUTO_INCREMENT,
  `donor_id` int DEFAULT NULL,
  `datetime_created` datetime NOT NULL,
  `transport_mode` int DEFAULT NULL,
  `number_of_items` int NOT NULL,
  `is_posted` tinyint(1) DEFAULT 1,
  `is_collected` tinyint(1) DEFAULT 0,
  `is_distributed` tinyint(1) DEFAULT 0,
  `street` varchar(100) NOT NULL,
  `barangay` varchar(100) NOT NULL,
  `city` varchar(100) NOT NULL,
  `caption` TEXT NOT NULL,
  PRIMARY KEY (`donation_id`),
  KEY `donor_id` (`donor_id`),
  KEY `transport_mode` (`transport_mode`),
  CONSTRAINT `donations_ibfk_1` FOREIGN KEY (`donor_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `donations_ibfk_3` FOREIGN KEY (`transport_mode`) REFERENCES `transport_modes` (`mode_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `items` (
  `item_id` int NOT NULL AUTO_INCREMENT,
  `donation_id` int DEFAULT NULL,
  `category` int DEFAULT NULL,
  `quantity` int NOT NULL,
  `unit` varchar(50) NOT NULL,
  `item_img_url` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`item_id`),
  KEY `category` (`category`),
  KEY `donation_id` (`donation_id`),
  CONSTRAINT `items_ibfk_1` FOREIGN KEY (`category`) REFERENCES `categories` (`category_id`),
  CONSTRAINT `items_ibfk_2` FOREIGN KEY (`donation_id`) REFERENCES `donations` (`donation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `reserved_donations` (
  `reserved_donation_id` int AUTO_INCREMENT,
  `donation_id` int DEFAULT NULL,
  `collector_id` int DEFAULT NULL,
  `datetime_reserved` datetime NOT NULL,
  `is_collected` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`reserved_donation_id`),
  KEY `donation_id` (`donation_id`),
  KEY `collector_id` (`collector_id`),
  CONSTRAINT `reserved_donations_ibfk_1` FOREIGN KEY (`donation_id`) REFERENCES `donations` (`donation_id`),
  CONSTRAINT `reserved_donations_ibfk_2` FOREIGN KEY (`collector_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `collected_donations` (
  `collected_donation_id` int AUTO_INCREMENT,
  `donation_id` int DEFAULT NULL,
  `collector_id` int DEFAULT NULL,
  `is_distributed` tinyint(1) DEFAULT NULL,
  `datetime_collected` datetime NOT NULL,
  PRIMARY KEY (`collected_donation_id`),
  KEY `donation_id` (`donation_id`),
  KEY `collector_id` (`collector_id`),
  CONSTRAINT `collected_donations_ibfk_1` FOREIGN KEY (`donation_id`) REFERENCES `donations` (`donation_id`),
  CONSTRAINT `collected_donations_ibfk_2` FOREIGN KEY (`collector_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `distributed_donations` (
  `distributed_donation_id` int AUTO_INCREMENT,
  `donation_id` int DEFAULT NULL,
  `collector_id` int DEFAULT NULL,
  `datetime_distributed` datetime NOT NULL,
  PRIMARY KEY (`distributed_donation_id`),
  KEY `donation_id` (`donation_id`),
  KEY `collector_id` (`collector_id`),
  CONSTRAINT `distributed_donations_ibfk_1` FOREIGN KEY (`donation_id`) REFERENCES `donations` (`donation_id`),
  CONSTRAINT `distributed_donations_ibfk_2` FOREIGN KEY (`collector_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `distribution_images` (
  `image_id` int NOT NULL AUTO_INCREMENT,
  `donation_id` int DEFAULT NULL,
  `image_link` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`image_id`),
  KEY `donation_id` (`donation_id`),
  CONSTRAINT `distribution_images_ibfk_1` FOREIGN KEY (`donation_id`) REFERENCES `donations` (`donation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `events` (
  `event_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `description` varchar(200) NOT NULL,
  `start_datetime` datetime DEFAULT NULL,
  `due_datetime` datetime DEFAULT NULL,
  `collector_id` int DEFAULT NULL,
  PRIMARY KEY (`event_id`),
  KEY `collector_id` (`collector_id`),
  CONSTRAINT `events_ibfk_1` FOREIGN KEY (`collector_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `event_donations` (
  `event_donation_id` int NOT NULL AUTO_INCREMENT,
  `event_id` int DEFAULT NULL,
  `donor_id` int DEFAULT NULL,
  `donation_id` int DEFAULT NULL,
  PRIMARY KEY (`event_donation_id`),
  KEY `event_id` (`event_id`),
  KEY `donor_id` (`donor_id`),
  KEY `donation_id` (`donation_id`),
  CONSTRAINT `event_donations_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `events` (`event_id`),
  CONSTRAINT `event_donations_ibfk_2` FOREIGN KEY (`donor_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `event_donations_ibfk_3` FOREIGN KEY (`donation_id`) REFERENCES `donations` (`donation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `item_images` (
  `image_id` int NOT NULL AUTO_INCREMENT,
  `item_id` int DEFAULT NULL,
  `image_link` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`image_id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `item_images_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `items` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `members` (
  `member_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `collector_id` int DEFAULT NULL,
  PRIMARY KEY (`member_id`),
  KEY `user_id` (`user_id`),
  KEY `collector_id` (`collector_id`),
  CONSTRAINT `members_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `members_ibfk_2` FOREIGN KEY (`collector_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `invites` (
  `invite_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `collector_id` int DEFAULT NULL,
  PRIMARY KEY (`invite_id`),
  KEY `user_id` (`user_id`),
  KEY `collector_id` (`collector_id`),
  CONSTRAINT `invites_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `invites_ibfk_2` FOREIGN KEY (`collector_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
