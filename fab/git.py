# -*- coding: utf-8 -*-

import os

from fabric.api import settings, sudo as fab_sudo

from shell import runcmd


GIT_USER = "git-web"
GIT_GROUP = "git-web"
GIT_HOME = "/srv/www"


def sudo(args):
    fab_sudo("%s" % args, pty=True, user=GIT_USER)


def install_git():
    runcmd('apt-get -y install git')


def create_user():
    with settings(warn_only=True):
        runcmd('adduser '
               '--home={home} --disabled-password '
               '--gecos "" '
               '{username}'.format(username=GIT_USER, home=GIT_HOME))


def home(name):
    return os.path.join(GIT_HOME, name)


def clone(url, name):
    with settings(warn_only=True):
        sudo('git clone %s %s' %
             (url, os.path.join(GIT_HOME, name)))
