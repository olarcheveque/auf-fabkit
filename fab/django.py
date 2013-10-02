# -*- coding: utf-8 -*-

import ssl
import git
import apache
import mysql


def provision(fqdn, idp_fqdn=None):
    db_name = fqdn.replace('.', '-')

    ssl.install_openssl()
    ssl.create_certificats(fqdn)

    git.install_git()
    git.create_user()

    apache.install_apache()
    apache.add_mod_rewrite()
    apache.add_mod_ssl()
    apache.add_mod_wsgi()
    apache.add_mod_mellon()

    extra = {}
    if idp_fqdn:
        ssl.create_certificats(idp_fqdn)
        apache.add_vhost(idp_fqdn, 'vhost_idp.txt')
        extra = {'idp': idp_fqdn, }

    apache.add_vhost(fqdn, 'vhost_wsgi_mellon.txt', extra)

    apache.restart()

    mysql.install_mysql()
    mysql.setup_db(db_name)
