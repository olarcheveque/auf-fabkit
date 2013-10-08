# -*- coding: utf-8 -*-
"""
Module git
==========

Ce module fournit les fonctions pour mettre en place git et l'utiliser selon
des conventions.

"""

import os
import datetime

from fabric.api import cd, settings, sudo as fab_sudo

from utils import runcmd

#: compte du user git
GIT_USER = "git-web"

#: groupe du user git
GIT_GROUP = "git-web"

#: home du user git
GIT_HOME = "/srv/www"

#: Fichier contenant les logs de commandes relative à git
GIT_LOG = os.path.join(GIT_HOME, 'logs')


def sudo(args):
    """
    Helper pour exécuter sur le serveur une commande en tant que le user git
    """
    fab_sudo("%s" % args, pty=True, user=GIT_USER)


def install():
    """
    Installation du paquet git
    Création du user git
    Création du home de git
    """
    runcmd('apt-get -y install git')
    create_user()
    with settings(warn_only=True):
        sudo('mkdir %s' % GIT_LOG)


def create_user():
    """
    Création du user git
    """
    with settings(warn_only=True):
        runcmd('adduser '
               '--home={home} --disabled-password '
               '--gecos "" '
               '{username}'.format(username=GIT_USER, home=GIT_HOME))


def home(name):
    """
    Return le path absolu du projet *name*
    """
    return os.path.join(GIT_HOME, name)


def clone(url, name):
    """
    Clone un projet *name* en utilisant l'*url* du dépôt git
    """
    with settings(warn_only=True):
        sudo('git clone %s %s' %
             (url, os.path.join(GIT_HOME, name)))


def checkout(name, branch='master'):
    """
    Fait un checkout du projet *name* selon une *branch* spécifique
    """
    path = home(name)
    with cd(path):
        sudo('git pull')
        sudo('git checkout %s' % branch)
        now, dummy = unicode(datetime.datetime.now()).\
            replace(' ', '_').split('.')
        output = '%s/%s-%s-%s.txt' % (GIT_LOG, now, name, branch)
        sudo('git log -n 1 --oneline > %s' % output)
