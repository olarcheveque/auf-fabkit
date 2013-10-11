# -*- coding: utf-8 -*-
"""
Module utils
============

Ce module contient des fonctions utilisées par les autres modules.

"""


import os

from fabric.api import sudo

#: répertoire où sont stockés les templates à mapper
TPL_DIR = os.path.join(os.path.dirname(__file__), 'tpl')

#: mot de passe par défaut de vagrant
FABRIC_ENV_PASSWORD = "vagrant"

#: définition du rôle 'vagrant'
FABRIC_ENV_ROLEDEFS = {
    'vagrant': ['vagrant@127.0.0.1:2222', ],
    }

# Montage FS du répertoire partagé avec la VM
VAGRANT_SHARED_ROOT = '/vagrant'

# user vagrant dans VM
VAGRANT_USER = 'vagrant'

# group vagrant dans VM
VAGRANT_GROUP = 'vagrant'


def runcmd(arg):
    """
    Wrapper de la commande sudo pour activer le pty
    """
    sudo("%s" % arg, pty=True)


def setup_fabric(env):
    """
    Configuration de l'*env* (fabric.api.env) pour travailler avec vagrant
    """
    env.password = FABRIC_ENV_PASSWORD
    env.roledefs.update(FABRIC_ENV_ROLEDEFS)
