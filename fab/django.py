# -*- coding: utf-8 -*-

import ssl
import git
import apache
import mysql
import venv
import idp


def setup_web_stack():
    ssl.install_openssl()

    git.install_git()
    git.create_user()

    apache.install_apache()
    apache.add_mod_rewrite()
    apache.add_mod_ssl()
    apache.add_mod_wsgi()
    apache.add_mod_mellon()

    mysql.install_mysql()
    venv.install_virtualenv()


def setup_mellon_site(fqdn, idp_fqdn):
    db_name = fqdn.replace('.', '_')
    mysql.setup_db(db_name)
    extra = {'idp': idp_fqdn, }
    ssl.create_certificats(fqdn)
    apache.add_vhost(fqdn, 'vhost_wsgi_mellon.txt', extra)


def provision(fqdn, idp_fqdn=None):
    setup_web_stack()
    idp.setup(idp_fqdn)
    #setup_mellon_site(fqdn, idp_fqdn)
    apache.restart()
