# -*- coding: utf-8 -*-

from shell import runcmd


def install_deb_toolkit():
    """
    Kit pour construire les paquets deb
    """
    runcmd('apt-get install -y '
           'devscripts '
           'dpkg-dev '
           'dput '
           'fakeroot '
           'debhelper '
           'build-essential')
