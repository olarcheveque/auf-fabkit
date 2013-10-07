# -*- coding: utf-8 -*-

import os

from fabric.contrib.files import upload_template

from git import GIT_HOME
from shell import runcmd, TPL_DIR

import mellon

APACHE_VHOST_DIR = '/etc/apache2/sites-available/'


def get_home_sites():
    return GIT_HOME


def install():
    runcmd('apt-get -y install apache2')


def add_mod_rewrite():
    runcmd('a2enmod rewrite')


def add_mod_ssl():
    runcmd('a2enmod ssl')


def add_mod_wsgi():
    runcmd('apt-get -y install libapache2-mod-wsgi')
    runcmd('a2enmod wsgi')


def add_mod_mellon():
    mellon.install_build_deps()
    mellon.build_mellon()
    mellon.install_mellon()
    runcmd('a2enmod auth_mellon')


def graceful():
    runcmd('/etc/init.d/apache2 graceful')


def restart():
    runcmd('/etc/init.d/apache2 restart')


def add_vhost(fqdn, filename, extra_context={}):
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
