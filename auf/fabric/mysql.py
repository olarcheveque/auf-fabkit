# -*- coding: utf-8 -*-
"""
Module MySQL
============

Module qui permet de d'installer et de configurer un serveur de base de données
MySQL.
"""

import os
import MySQLdb

from getpass import getpass

from fabric.api import settings, prompt

from utils import runcmd

# Version de MySQL (wheezy)
MYSQL_VERSION = "5.5"

# User Root
MYSQL_ROOT_USER = "root"

# Password Root
MYSQL_ROOT_PASSWORD = "root"

# Adresse du serveur IP (pour accéder en mode TCP)
MYSQL_P_HOST = '127.0.0.1'


MYSQL_DUMP_HOST = None
MYSQL_DUMP_PORT = None
MYSQL_DUMP_USER = None
MYSQL_DUMP_PASS = None


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


def get_db_access():
    global MYSQL_DUMP_HOST, MYSQL_DUMP_PORT, MYSQL_DUMP_USER, MYSQL_DUMP_PASS
    if MYSQL_DUMP_HOST is None or \
       MYSQL_DUMP_PORT is None or \
       MYSQL_DUMP_USER is None or \
       MYSQL_DUMP_PASS is None:
        MYSQL_DUMP_HOST = prompt('Host MySQL', default='db.auf')
        MYSQL_DUMP_PORT = prompt('Port MySQL', default='3306')
        MYSQL_DUMP_USER = prompt('User MySQL')
        MYSQL_DUMP_PASS = getpass('Pass MySQL')
    return {
        'host': MYSQL_DUMP_HOST,
        'port': MYSQL_DUMP_PORT,
        'user': MYSQL_DUMP_USER,
        'password': MYSQL_DUMP_PASS,
        'cursor': MySQLdb.connect(host=MYSQL_DUMP_HOST,
                                  user=MYSQL_DUMP_USER,
                                  passwd=MYSQL_DUMP_PASS,
                                  port=int(MYSQL_DUMP_PORT)).cursor()
        }


def get_tables(db):
    """
    Retourne la liste de tables de la base de donnée *db*
    """
    conf = get_db_access()
    cursor = conf['cursor']
    cursor.execute("USE %s" % db)
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    return [t[0] for t in tables]


def dump_export(db, out=None):
    """
    Créer un dump SQL d'une base de données *db* distante
    *out* est le fichier optionnel de sortie, par défaut host_db.sql
    """
    print "Votre accès pour faire le dump"
    conf = get_db_access()
    if out is None:
        out = "%s_%s.sql" % (conf['host'], db)
    if os.path.exists(out):
        return out
    tables = [t for t in get_tables(db) if not t.startswith('ref')]
    conf.update({
        'db': db,
        'tables': " ".join(tables),
        'out': out,
        })

    cmd = "mysqldump  --no-create-db --lock-tables=false \
    %(db)s %(tables)s --user=%(user)s --password=%(password)s \
    --host=%(host)s --port=%(port)s > %(out)s" % conf
    os.system(cmd)
    return out
