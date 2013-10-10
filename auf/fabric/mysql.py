# -*- coding: utf-8 -*-
"""
Module MySQL
============

Module qui permet de d'installer et de configurer un serveur de base de données
MySQL.
"""


from fabric.api import settings

from utils import runcmd

# Version de MySQL (wheezy)
MYSQL_VERSION = "5.5"

# User Root
MYSQL_ROOT_USER = "root"

# Password Root
MYSQL_ROOT_PASSWORD = "root"

# Adresse du serveur IP (pour accéder en mode TCP)
MYSQL_P_HOST = '127.0.0.1'


def install():
    """
    Installe le serveur MySQL selon des accès prédéfinis
    """
    runcmd('debconf-set-selections <<< \'mysql-server-{version} '
           'mysql-server/root_password password {password}\''.format(
               password=MYSQL_ROOT_PASSWORD,
               version=MYSQL_VERSION))
    runcmd('debconf-set-selections <<< \'mysql-server-{version} '
           'mysql-server/root_password_again password {password}\''.format(
               password=MYSQL_ROOT_PASSWORD,
               version=MYSQL_VERSION))

    runcmd('apt-get -y install mysql-server')


def create_user(user):
    """
    Création d'un utilisateur *user* avec un mode de passe identique à *user*
    """
    with settings(warn_only=True):
        runcmd('mysql --user={root} --password={password} '
               '--execute="CREATE USER '
               '\'{user}\' IDENTIFIED BY \'{userpass}\'"'
               .format(root=MYSQL_ROOT_USER,
                       password=MYSQL_ROOT_PASSWORD,
                       user=user,
                       userpass=user))


def create_database(db):
    """
    Création d'une base de donnée nommée *db*
    """
    with settings(warn_only=True):
        runcmd('mysql '
               '--user={root} '
               '--password={password} '
               '--execute="create database {database}"'
               .format(root=MYSQL_ROOT_USER,
                       password=MYSQL_ROOT_PASSWORD,
                       database=db))


def grant_user(db):
    """
    donner toutes les permissions au user *db* sur la base de données *db*.
    """
    runcmd('mysql --user={root} --password={password} '
           '--execute="GRANT ALL ON {database}.* TO '
           '\'{user}\'@\'127.0.0.1\' IDENTIFIED BY \'{userpass}\'"'
           .format(root=MYSQL_ROOT_USER,
                   password=MYSQL_ROOT_PASSWORD,
                   database=db,
                   user=db,
                   userpass=db))


def setup_db(db):
    """
    Créer un user *db*
    Créer une base de données *db*
    Donner tous les privilèges à l'utilisateur *db* sur la base de données *db*
    """
    create_user(db)
    create_database(db)
    grant_user(db)
