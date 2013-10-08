# -*- coding: utf-8 -*-

from fabric.api import settings

from utils import runcmd

MYSQL_VERSION = "5.5"
MYSQL_ROOT_USER = "root"
MYSQL_ROOT_PASSWORD = "root"

MYSQL_P_HOST = '127.0.0.1'


def install():
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
    with settings(warn_only=True):
        runcmd('mysql --user={root} --password={password} '
               '--execute="CREATE USER '
               '\'{user}\' IDENTIFIED BY \'{userpass}\'"'
               .format(root=MYSQL_ROOT_USER,
                       password=MYSQL_ROOT_PASSWORD,
                       user=user,
                       userpass=user))


def create_database(db):
    with settings(warn_only=True):
        runcmd('mysql '
               '--user={root} '
               '--password={password} '
               '--execute="create database {database}"'
               .format(root=MYSQL_ROOT_USER,
                       password=MYSQL_ROOT_PASSWORD,
                       database=db))


def grant_user(db):
    runcmd('mysql --user={root} --password={password} '
           '--execute="GRANT ALL ON {database}.* TO '
           '\'{user}\'@\'127.0.0.1\' IDENTIFIED BY \'{userpass}\'"'
           .format(root=MYSQL_ROOT_USER,
                   password=MYSQL_ROOT_PASSWORD,
                   database=db,
                   user=db,
                   userpass=db))


def setup_db(db):
        create_user(db)
        create_database(db)
        grant_user(db)
