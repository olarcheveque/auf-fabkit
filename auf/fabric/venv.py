# -*- coding: utf-8 -*-

import os

from utils import runcmd

import git

VIRTUAL_ENVS = os.path.join(git.GIT_HOME, '.virtualenvs')


def install_virtualenv():
    runcmd('apt-get install -y python-virtualenv --force-yes')


def mkenv(project):
    path = os.path.join(VIRTUAL_ENVS, project)
    git.sudo('virtualenv --system-site-packages %s' % path)


def get_path(project):
    return os.path.join(VIRTUAL_ENVS, project)


def get_bin_path(project):
    return os.path.join(get_path(project), 'bin')


def get_bin_python(project):
    return os.path.join(get_bin_path(project), 'python')


def get_bin_pip(project):
    return os.path.join(get_bin_path(project), 'pip')
