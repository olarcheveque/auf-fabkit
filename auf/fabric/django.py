# -*- coding: utf-8 -*-
"""
Module Django
=============

Module qui permet de configurer une application Django pour fonctionner avec un
frontal Web.
"""

from utils import runcmd

import ssl
import idp
import apache


def setup_with_mellon(fqdn, wsgi,
                      vhost_tpl="django_mellon_vhost.txt"):
    """
    """
    ssl.create_certificats(fqdn)
    idp.get_metadata()
    idp.register_sp(fqdn)
    extra = {
        'idp_fqdn': idp.FQDN,
        'wsgi': wsgi,
        }
    with(apache.get_home_sites()):
        runcmd('ln -s /vagrant %s' % fqdn)
    apache.add_vhost(fqdn, vhost_tpl, extra)
