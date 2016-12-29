-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Client :  localhost
-- Généré le :  Jeu 29 Décembre 2016 à 15:51
-- Version du serveur :  5.7.16-0ubuntu0.16.04.1
-- Version de PHP :  7.0.8-0ubuntu0.16.04.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `votes_master`
--

-- --------------------------------------------------------

--
-- Structure de la table `demo`
--

CREATE TABLE `demo` (
  `numero` int(11) NOT NULL,
  `titre` varchar(256) COLLATE utf8_unicode_ci NOT NULL,
  `description` text COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `poster`
--

CREATE TABLE `poster` (
  `numero` int(11) NOT NULL,
  `titre` varchar(256) COLLATE utf8_unicode_ci NOT NULL,
  `description` text COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `utilisateur`
--

CREATE TABLE `utilisateur` (
  `hash_fp` varchar(256) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `vote_demo`
--

CREATE TABLE `vote_demo` (
  `id_utilisateur` varchar(256) COLLATE utf8_unicode_ci NOT NULL,
  `numero_demo` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `vote_poster`
--

CREATE TABLE `vote_poster` (
  `id_utilisateur` varchar(256) COLLATE utf8_unicode_ci NOT NULL,
  `numero_poster` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Index pour les tables exportées
--

--
-- Index pour la table `demo`
--
ALTER TABLE `demo`
  ADD PRIMARY KEY (`numero`);

--
-- Index pour la table `poster`
--
ALTER TABLE `poster`
  ADD PRIMARY KEY (`numero`);

--
-- Index pour la table `utilisateur`
--
ALTER TABLE `utilisateur`
  ADD PRIMARY KEY (`hash_fp`);

--
-- Index pour la table `vote_demo`
--
ALTER TABLE `vote_demo`
  ADD PRIMARY KEY (`id_utilisateur`,`numero_demo`),
  ADD KEY `numero_demo` (`numero_demo`);

--
-- Index pour la table `vote_poster`
--
ALTER TABLE `vote_poster`
  ADD PRIMARY KEY (`id_utilisateur`,`numero_poster`),
  ADD KEY `numero_poster` (`numero_poster`);

--
-- Contraintes pour les tables exportées
--

--
-- Contraintes pour la table `vote_demo`
--
ALTER TABLE `vote_demo`
  ADD CONSTRAINT `vote_demo_ibfk_1` FOREIGN KEY (`id_utilisateur`) REFERENCES `utilisateur` (`hash_fp`),
  ADD CONSTRAINT `vote_demo_ibfk_2` FOREIGN KEY (`numero_demo`) REFERENCES `demo` (`numero`);

--
-- Contraintes pour la table `vote_poster`
--
ALTER TABLE `vote_poster`
  ADD CONSTRAINT `vote_poster_ibfk_1` FOREIGN KEY (`id_utilisateur`) REFERENCES `utilisateur` (`hash_fp`),
  ADD CONSTRAINT `vote_poster_ibfk_2` FOREIGN KEY (`numero_poster`) REFERENCES `poster` (`numero`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
