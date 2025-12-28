-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : dim. 28 déc. 2025 à 10:55
-- Version du serveur : 8.0.32
-- Version de PHP : 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `edt_faculte`
--

-- --------------------------------------------------------

--
-- Structure de la table `administrateur`
--

DROP TABLE IF EXISTS `administrateur`;
CREATE TABLE IF NOT EXISTS `administrateur` (
  `id_admin` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) NOT NULL,
  `prenom` varchar(50) NOT NULL,
  PRIMARY KEY (`id_admin`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `administrateur`
--

INSERT INTO `administrateur` (`id_admin`, `nom`, `prenom`) VALUES
(1, 'Lemoine', 'Marc'),
(2, 'Bernard', 'Sophie'),
(3, 'Faure', 'Lucie'),
(4, 'Girard', 'Olivier'),
(5, 'Henry', 'Marie');

-- --------------------------------------------------------

--
-- Structure de la table `chef_departement`
--

DROP TABLE IF EXISTS `chef_departement`;
CREATE TABLE IF NOT EXISTS `chef_departement` (
  `id_chef` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) NOT NULL,
  `prenom` varchar(50) NOT NULL,
  `id_departement` int NOT NULL,
  PRIMARY KEY (`id_chef`),
  KEY `fk_chef_dept` (`id_departement`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `chef_departement`
--

INSERT INTO `chef_departement` (`id_chef`, `nom`, `prenom`, `id_departement`) VALUES
(1, 'Mohamed', 'Karim', 1),
(2, 'Sofia', 'Lina', 2),
(3, 'Amine', 'Yassine', 3),
(4, 'Leila', 'Nora', 4),
(5, 'Omar', 'Samir', 5);

-- --------------------------------------------------------

--
-- Structure de la table `departement`
--

DROP TABLE IF EXISTS `departement`;
CREATE TABLE IF NOT EXISTS `departement` (
  `id_departement` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  PRIMARY KEY (`id_departement`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `departement`
--

INSERT INTO `departement` (`id_departement`, `nom`) VALUES
(1, 'Informatique'),
(2, 'Mathématiques'),
(3, 'Physique'),
(4, 'Chimie'),
(5, 'Biologie');

-- --------------------------------------------------------

--
-- Structure de la table `doyen`
--

DROP TABLE IF EXISTS `doyen`;
CREATE TABLE IF NOT EXISTS `doyen` (
  `id_doyen` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) NOT NULL,
  `prenom` varchar(50) NOT NULL,
  PRIMARY KEY (`id_doyen`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `doyen`
--

INSERT INTO `doyen` (`id_doyen`, `nom`, `prenom`) VALUES
(1, 'Dupont', 'Jean'),
(2, 'Martin', 'Claire'),
(3, 'Petit', 'Luc'),
(4, 'Moreau', 'Alice'),
(5, 'Rousseau', 'Paul');

-- --------------------------------------------------------

--
-- Structure de la table `edt_validation`
--

DROP TABLE IF EXISTS `edt_validation`;
CREATE TABLE IF NOT EXISTS `edt_validation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `valide` tinyint(1) DEFAULT '0',
  `date_validation` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `edt_validation`
--

INSERT INTO `edt_validation` (`id`, `valide`, `date_validation`) VALUES
(1, 1, '2025-12-28 10:15:44'),
(2, 1, '2025-12-28 10:15:50');

-- --------------------------------------------------------

--
-- Structure de la table `etudiant`
--

DROP TABLE IF EXISTS `etudiant`;
CREATE TABLE IF NOT EXISTS `etudiant` (
  `id_etudiant` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) NOT NULL,
  `prenom` varchar(50) NOT NULL,
  `id_formation` int NOT NULL,
  PRIMARY KEY (`id_etudiant`),
  KEY `id_formation` (`id_formation`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `etudiant`
--

INSERT INTO `etudiant` (`id_etudiant`, `nom`, `prenom`, `id_formation`) VALUES
(1, 'Benali', 'Amine', 1),
(2, 'Bouaziz', 'Sara', 2),
(3, 'Khelifi', 'Rania', 3),
(4, 'Mansouri', 'Youssef', 4),
(5, 'Ait Ahmed', 'Leila', 5);

-- --------------------------------------------------------

--
-- Structure de la table `examen`
--

DROP TABLE IF EXISTS `examen`;
CREATE TABLE IF NOT EXISTS `examen` (
  `id_examen` int NOT NULL AUTO_INCREMENT,
  `id_module` int NOT NULL,
  `date_exam` date NOT NULL,
  `duree` int NOT NULL,
  `id_salle` int NOT NULL,
  `id_prof` int NOT NULL,
  `heure_debut` time DEFAULT NULL,
  `heure_fin` time DEFAULT NULL,
  PRIMARY KEY (`id_examen`),
  KEY `id_module` (`id_module`),
  KEY `id_salle` (`id_salle`),
  KEY `id_prof` (`id_prof`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `examen`
--

INSERT INTO `examen` (`id_examen`, `id_module`, `date_exam`, `duree`, `id_salle`, `id_prof`, `heure_debut`, `heure_fin`) VALUES
(1, 1, '2026-01-10', 3, 1, 1, '09:00:00', '11:00:00'),
(2, 2, '2026-01-10', 2, 2, 4, '09:00:00', '11:00:00'),
(3, 3, '2026-01-12', 3, 3, 2, '09:00:00', '12:00:00'),
(4, 4, '2026-01-13', 3, 4, 3, '12:00:00', '14:00:00'),
(5, 5, '2026-01-14', 2, 5, 5, '09:00:00', '11:00:00'),
(30, 3, '2026-01-16', 2, 3, 3, '10:00:00', '12:00:00'),
(31, 4, '2026-01-16', 2, 4, 3, '12:00:00', '14:00:00'),
(32, 6, '2025-12-27', 3, 1, 1, NULL, NULL),
(33, 7, '2025-12-28', 3, 1, 1, NULL, NULL),
(34, 1, '2026-01-15', 2, 1, 1, '09:00:00', '11:00:00'),
(35, 2, '2026-01-15', 2, 2, 2, '09:00:00', '11:00:00');

-- --------------------------------------------------------

--
-- Structure de la table `formation`
--

DROP TABLE IF EXISTS `formation`;
CREATE TABLE IF NOT EXISTS `formation` (
  `id_formation` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `id_departement` int NOT NULL,
  PRIMARY KEY (`id_formation`),
  KEY `id_departement` (`id_departement`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `formation`
--

INSERT INTO `formation` (`id_formation`, `nom`, `id_departement`) VALUES
(1, 'Licence CS', 1),
(2, 'Master CS', 1),
(3, 'Licence Math', 2),
(4, 'Master Math', 2),
(5, 'Licence Physique', 3);

-- --------------------------------------------------------

--
-- Structure de la table `inscription`
--

DROP TABLE IF EXISTS `inscription`;
CREATE TABLE IF NOT EXISTS `inscription` (
  `id_etudiant` int NOT NULL,
  `id_module` int NOT NULL,
  PRIMARY KEY (`id_etudiant`,`id_module`),
  KEY `id_module` (`id_module`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `inscription`
--

INSERT INTO `inscription` (`id_etudiant`, `id_module`) VALUES
(1, 1),
(1, 2),
(2, 3),
(3, 3),
(4, 5),
(3, 6),
(3, 7);

-- --------------------------------------------------------

--
-- Structure de la table `module`
--

DROP TABLE IF EXISTS `module`;
CREATE TABLE IF NOT EXISTS `module` (
  `id_module` int NOT NULL AUTO_INCREMENT,
  `nom_module` varchar(100) NOT NULL,
  `id_formation` int NOT NULL,
  `duree` int DEFAULT NULL,
  PRIMARY KEY (`id_module`),
  KEY `id_formation` (`id_formation`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `module`
--

INSERT INTO `module` (`id_module`, `nom_module`, `id_formation`, `duree`) VALUES
(1, 'Algorithmique', 1, 3),
(2, 'Réseaux', 1, 2),
(3, 'Statistiques', 3, 3),
(4, 'Physique 1', 5, 3),
(5, 'Math Avancée', 4, 2),
(6, 'Analyse', 3, 3),
(7, 'Algebre', 3, 3);

-- --------------------------------------------------------

--
-- Structure de la table `passage_examen`
--

DROP TABLE IF EXISTS `passage_examen`;
CREATE TABLE IF NOT EXISTS `passage_examen` (
  `id_etudiant` int NOT NULL,
  `id_examen` int NOT NULL,
  PRIMARY KEY (`id_etudiant`,`id_examen`),
  KEY `id_examen` (`id_examen`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `passage_examen`
--

INSERT INTO `passage_examen` (`id_etudiant`, `id_examen`) VALUES
(1, 1),
(1, 2),
(2, 3),
(3, 3),
(4, 5);

-- --------------------------------------------------------

--
-- Structure de la table `professeur`
--

DROP TABLE IF EXISTS `professeur`;
CREATE TABLE IF NOT EXISTS `professeur` (
  `id_prof` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) NOT NULL,
  `prenom` varchar(50) NOT NULL,
  `id_departement` int NOT NULL,
  PRIMARY KEY (`id_prof`),
  KEY `id_departement` (`id_departement`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `professeur`
--

INSERT INTO `professeur` (`id_prof`, `nom`, `prenom`, `id_departement`) VALUES
(1, 'Ahmed', 'Ali', 1),
(2, 'Salima', 'Nora', 2),
(3, 'Hassan', 'Meryem', 3),
(4, 'Leila', 'Karim', 1),
(5, 'Omar', 'Sophie', 2);

-- --------------------------------------------------------

--
-- Structure de la table `salle`
--

DROP TABLE IF EXISTS `salle`;
CREATE TABLE IF NOT EXISTS `salle` (
  `id_salle` int NOT NULL AUTO_INCREMENT,
  `nom_salle` varchar(50) NOT NULL,
  `capacite` int NOT NULL,
  `type_salle` varchar(20) NOT NULL,
  PRIMARY KEY (`id_salle`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `salle`
--

INSERT INTO `salle` (`id_salle`, `nom_salle`, `capacite`, `type_salle`) VALUES
(1, 'A101', 30, 'normale'),
(2, 'Amph1', 200, 'amphi'),
(3, 'B202', 30, 'normale'),
(4, 'C101', 30, 'normale'),
(5, 'Amph2', 200, 'amphi');

-- --------------------------------------------------------

--
-- Structure de la table `surveillance`
--

DROP TABLE IF EXISTS `surveillance`;
CREATE TABLE IF NOT EXISTS `surveillance` (
  `id_prof` int NOT NULL,
  `id_examen` int NOT NULL,
  PRIMARY KEY (`id_prof`,`id_examen`),
  KEY `id_examen` (`id_examen`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `surveillance`
--

INSERT INTO `surveillance` (`id_prof`, `id_examen`) VALUES
(4, 1),
(1, 2),
(5, 3);

-- --------------------------------------------------------

--
-- Structure de la table `validation_edt`
--

DROP TABLE IF EXISTS `validation_edt`;
CREATE TABLE IF NOT EXISTS `validation_edt` (
  `id_validation` int NOT NULL AUTO_INCREMENT,
  `date_validation` date NOT NULL,
  `heure_validation` time NOT NULL,
  `valide_par` varchar(50) NOT NULL,
  PRIMARY KEY (`id_validation`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `validation_edt`
--

INSERT INTO `validation_edt` (`id_validation`, `date_validation`, `heure_validation`, `valide_par`) VALUES
(1, '2025-12-28', '10:23:40', 'Doyen'),
(2, '2025-12-28', '10:24:09', 'Doyen'),
(3, '2025-12-28', '10:36:03', 'Doyen');

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `chef_departement`
--
ALTER TABLE `chef_departement`
  ADD CONSTRAINT `fk_chef_dept` FOREIGN KEY (`id_departement`) REFERENCES `departement` (`id_departement`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `etudiant`
--
ALTER TABLE `etudiant`
  ADD CONSTRAINT `etudiant_ibfk_1` FOREIGN KEY (`id_formation`) REFERENCES `formation` (`id_formation`);

--
-- Contraintes pour la table `examen`
--
ALTER TABLE `examen`
  ADD CONSTRAINT `examen_ibfk_1` FOREIGN KEY (`id_module`) REFERENCES `module` (`id_module`),
  ADD CONSTRAINT `examen_ibfk_2` FOREIGN KEY (`id_salle`) REFERENCES `salle` (`id_salle`),
  ADD CONSTRAINT `examen_ibfk_3` FOREIGN KEY (`id_prof`) REFERENCES `professeur` (`id_prof`);

--
-- Contraintes pour la table `formation`
--
ALTER TABLE `formation`
  ADD CONSTRAINT `formation_ibfk_1` FOREIGN KEY (`id_departement`) REFERENCES `departement` (`id_departement`);

--
-- Contraintes pour la table `inscription`
--
ALTER TABLE `inscription`
  ADD CONSTRAINT `inscription_ibfk_1` FOREIGN KEY (`id_etudiant`) REFERENCES `etudiant` (`id_etudiant`),
  ADD CONSTRAINT `inscription_ibfk_2` FOREIGN KEY (`id_module`) REFERENCES `module` (`id_module`);

--
-- Contraintes pour la table `module`
--
ALTER TABLE `module`
  ADD CONSTRAINT `module_ibfk_1` FOREIGN KEY (`id_formation`) REFERENCES `formation` (`id_formation`);

--
-- Contraintes pour la table `passage_examen`
--
ALTER TABLE `passage_examen`
  ADD CONSTRAINT `passage_examen_ibfk_1` FOREIGN KEY (`id_etudiant`) REFERENCES `etudiant` (`id_etudiant`),
  ADD CONSTRAINT `passage_examen_ibfk_2` FOREIGN KEY (`id_examen`) REFERENCES `examen` (`id_examen`);

--
-- Contraintes pour la table `professeur`
--
ALTER TABLE `professeur`
  ADD CONSTRAINT `professeur_ibfk_1` FOREIGN KEY (`id_departement`) REFERENCES `departement` (`id_departement`);

--
-- Contraintes pour la table `surveillance`
--
ALTER TABLE `surveillance`
  ADD CONSTRAINT `surveillance_ibfk_1` FOREIGN KEY (`id_prof`) REFERENCES `professeur` (`id_prof`),
  ADD CONSTRAINT `surveillance_ibfk_2` FOREIGN KEY (`id_examen`) REFERENCES `examen` (`id_examen`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
