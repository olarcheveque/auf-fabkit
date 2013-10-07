# -*- coding: utf-8 -*-

from fabric.contrib import files
from fabric.api import cd

from utils import runcmd
from debian import install_deb_toolkit


def install_build_deps():
    runcmd('apt-get install -y '
           'autotools-dev '
           'apache2-prefork-dev '
           'libcurl3-dev '
           'liblasso3-dev')


def build_mellon():
    if (files.exists('libapache2-mod-auth-mellon-0.6.1', use_sudo=True)):
        return
    install_deb_toolkit()
    install_build_deps()

    runcmd('dget -u http://non-gnu.uvt.nl/debian/wheezy/'
           'libapache2-mod-auth-mellon/'
           'libapache2-mod-auth-mellon_0.6.1-1.dsc')
    runcmd('dpkg-source -x libapache2-mod-auth-mellon_0.6.1-1.dsc')

    with cd('libapache2-mod-auth-mellon-0.6.1'):
        runcmd('dpkg-checkbuilddeps')
        runcmd('debuild -sa -us -uc')


def install_mellon():
    runcmd('dpkg -i libapache2-mod-auth-mellon_0.6.1-1_i386.deb')
