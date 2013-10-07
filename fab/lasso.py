# -*- coding: utf-8 -*-

from fabric.api import cd
from fabric.contrib import files

from debian import install_deb_toolkit

from shell import runcmd


def install_build_deps():
    runcmd('apt-get install -y '
           'python-all-dev '
           'fastjar '
           'python-central '
           'php5-dev '
           'python-lxml '
           'chrpath')


def build_lasso():
    if (files.exists('lasso_2.3.6-2.dsc', use_sudo=True)):
        return
    install_deb_toolkit()
    install_build_deps()

    runcmd('dget -u http://ftp.de.debian.org/debian'
           '/pool/main/l/lasso/lasso_2.3.6-2.dsc')
    runcmd('dpkg-source -x lasso_2.3.6-2.dsc')

    with cd('lasso-2.3.6'):
        runcmd('dpkg-checkbuilddeps')
        runcmd('debuild -sa -us -uc')


def install():
    runcmd('apt-get install -y python-lasso')
