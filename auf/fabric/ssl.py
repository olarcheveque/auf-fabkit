# -*- coding: utf-8 -*-
"""
Module SSL
==========

Module permettant d'installer openssl
et de créer des certifcats.
"""


from fabric.contrib import files

from utils import runcmd


def install():
    """
    Installe openssl
    """
    runcmd('apt-get -y install openssl')


def create_certificats(project):
    """
    Créer un certificat et une clef privée
    clef: /etc/ssl/private/saml-*project*-key.pem
    certificat: /etc/ssl/certs/saml-*project*-cert.pem
    """
    key = '/etc/ssl/private/saml-%s-key.pem' % project
    cert = '/etc/ssl/certs/saml-%s-cert.pem' % project
    if (files.exists(key, use_sudo=True) and
            files.exists(cert, use_sudo=True)):
        return

    runcmd("openssl req -new -x509 -keyout key.pem "
           "-out cert.pem -nodes -days 3650 -newkey rsa:2048 "
           "-subj '/CN=%s'" % project)
    runcmd('chmod 0600 key.pem')
    runcmd('chmod 0644 cert.pem')
    runcmd('chown root:root key.pem cert.pem')
    runcmd('mv key.pem %s' % key)
    runcmd('mv cert.pem %s' % cert)
