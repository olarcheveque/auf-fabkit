# -*- coding: utf-8 -*-

import os
import datetime

from fabric.api import cd, settings, sudo as fab_sudo

from utils import runcmd


GIT_USER = "git-web"
GIT_GROUP = "git-web"
GIT_HOME = "/srv/www"
GIT_LOG = os.path.join(GIT_HOME, 'logs')


def sudo(args):
    fab_sudo("%s" % args, pty=True, user=GIT_USER)


def install():
    runcmd('apt-get -y install git')
    create_user()
    with settings(warn_only=True):
        sudo('mkdir %s' % GIT_LOG)


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


def checkout(name, branch='master'):
    path = home(name)
    with cd(path):
        sudo('git pull')
        sudo('git checkout %s' % branch)
        now, dummy = unicode(datetime.datetime.now()).\
            replace(' ', '_').split('.')
        output = '%s/%s-%s-%s.txt' % (GIT_LOG, now, name, branch)
        sudo('git log -n 1 --oneline > %s' % output)
