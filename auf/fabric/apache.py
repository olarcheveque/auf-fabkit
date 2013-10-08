# -*- coding: utf-8 -*-
"""
Module Apache
=============

Module qui permet d'installer et de configurer des vhosts selon un gabarit.
Il offre des fonctions pour piloter le serveur web.
"""


import os

from fabric.contrib.files import upload_template

from git import GIT_HOME
from utils import runcmd, TPL_DIR

import mellon

#: Répertoire où sont déposés les fichiers vhost
APACHE_VHOST_DIR = '/etc/apache2/sites-available/'


def get_home_sites():
    """
    Retourne le path où sont installées les applications servies.
    """
    return GIT_HOME


def install():
    """
    Installe le paquet apache2
    """
    runcmd('apt-get -y install apache2')


def add_mod_rewrite():
    """
    Active le mod rewrite
    """
    runcmd('a2enmod rewrite')


def add_mod_ssl():
    """
    Active le mod rewrite
    """
    runcmd('a2enmod ssl')


def add_mod_wsgi():
    """
    Active le mod wsgi
    """
    runcmd('apt-get -y install libapache2-mod-wsgi')
    runcmd('a2enmod wsgi')


def add_mod_mellon():
    """
    Active le mod mellon
    (Note: présentement, ce module est compilé sur le serveur)
    """
    mellon.install_build_deps()
    mellon.build_mellon()
    mellon.install_mellon()
    runcmd('a2enmod auth_mellon')


def graceful():
    """
    Redémarrage en douceur
    """
    runcmd('/etc/init.d/apache2 graceful')


def restart():
    """
    Redémarrage bourrin
    """
    runcmd('/etc/init.d/apache2 restart')


def add_vhost(fqdn, filename, extra_context={}):
    """
    Création d'un vhost selon le template *filename* pour le projet *fqdn*.
    *project* et *project_path* sont disponibles dans le template mais vous
    pouvez en ajouter un aussi avec *extra_context*.
    """
    filename = os.path.join(TPL_DIR, filename)
    destination = os.path.join(APACHE_VHOST_DIR, fqdn)
    project_path = os.path.join(get_home_sites(), fqdn)
    data = {'project': fqdn, 'project_path': project_path, }
    data.update(extra_context)
    upload_template(
        filename,
        destination,
        context=data,
        use_sudo=True)
    runcmd('a2ensite %s' % fqdn)
