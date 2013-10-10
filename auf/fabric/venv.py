# -*- coding: utf-8 -*-
"""
Module venv
===========

Module qui permet de contrôler un environnement virtuel Python.
"""


import os

from utils import runcmd

import git

# Path où sont stockés les environnements virtuels
VIRTUAL_ENVS = os.path.join(git.GIT_HOME, '.virtualenvs')


def install_virtualenv():
    """
    Installe virtualenv
    """
    runcmd('apt-get install -y python-virtualenv --force-yes')


def mkenv(project):
    """
    Créer un environnement virtuel *project*
    """
    path = os.path.join(VIRTUAL_ENVS, project)
    git.sudo('virtualenv --system-site-packages %s' % path)


def get_path(project):
    """
    Récupérer le path de l'environnement virtuel du projet *project*
    """
    return os.path.join(VIRTUAL_ENVS, project)


def get_bin_path(project):
    """
    Récupérer le path du bin l'environnement virtuel du projet *project*
    """
    return os.path.join(get_path(project), 'bin')


def get_bin_python(project):
    """
    Récupérer l'interpréteur python du projet *project*
    """
    return os.path.join(get_bin_path(project), 'python')


def get_bin_pip(project):
    """
    Récupérer la commande pip du projet *project*
    """
    return os.path.join(get_bin_path(project), 'pip')
