# -*- coding: utf-8 -*-

import os

from fabric.api import cd
from fabric.contrib.files import upload_template

from utils import TPL_DIR, runcmd

import lasso
import ssl
import git
import apache
import mysql
import venv


def setup(idp_fqdn):
    # DEPS
    lasso.install()
    mysql.install()
    ssl.install()
    git.install()
    apache.install()
    apache.add_mod_rewrite()
    apache.add_mod_ssl()
    apache.add_mod_wsgi()
    venv.install_virtualenv()
    runcmd('apt-get install -y python-ldap')
    runcmd('apt-get install -y python-mysqldb --force-yes')

    # DB
    db_name = idp_fqdn.replace('.', '_')
    mysql.setup_db(db_name)

    # WEB
    ssl.create_certificats(idp_fqdn)
    extra = {'venv': venv.get_path(idp_fqdn), }
    apache.add_vhost(idp_fqdn, 'idp_vhost.txt', extra)

    # SOURCE
    git.clone('git://git.auf.org/authentic2', idp_fqdn)
    git.checkout(idp_fqdn, 'master')

    # VIRTUALENV
    venv.mkenv(idp_fqdn)
    bin_pip = venv.get_bin_pip(idp_fqdn)
    with cd(git.home(idp_fqdn)):
        git.sudo("%s install -r requirements.txt" % bin_pip)
        git.sudo("%s install django-auth-ldap" % bin_pip)

    # WSGI
    data = {
        'project_path': git.home(idp_fqdn),
        'venv': venv.get_path(idp_fqdn),
        }
    filename = os.path.join(TPL_DIR, 'idp_wsgi.txt')
    destination = os.path.join(venv.get_bin_path(idp_fqdn), 'idp_wsgi.py')
    upload_template(
        filename,
        destination,
        context=data,
        use_sudo=True,)
    runcmd('chown %s:%s %s' % (git.GIT_USER, git.GIT_GROUP, destination,))
    runcmd('chmod 644 %s' % (destination, ))

    # LOG file
    log_file = os.path.join(git.home(idp_fqdn), 'log.log')
    runcmd('touch %s' % log_file)
    runcmd('chmod g+w %s' % log_file)
    runcmd('chown %s:www-data %s' % (git.GIT_USER, log_file))

    # CONF
    data.update({
        'db_name': db_name,
        'db_user': db_name,
        'db_password': db_name,
        })
    filename = os.path.join(TPL_DIR, 'idp_local_settings.txt')
    destination = os.path.join(
        git.home(idp_fqdn),
        'aufcustom',
        'local_settings.py')
    upload_template(
        filename,
        destination,
        context=data,
        use_sudo=True,)
    runcmd('chown %s:%s %s' % (git.GIT_USER, git.GIT_GROUP, destination,))

    # manage.py
    data.update({
        'venv': venv.get_path(idp_fqdn),
        })
    filename = os.path.join(TPL_DIR, 'idp_manage.txt')
    destination = os.path.join(
        git.home(idp_fqdn),
        'manage.py')
    upload_template(
        filename,
        destination,
        context=data,
        use_sudo=True,)
    runcmd('chown %s:%s %s' % (git.GIT_USER, git.GIT_GROUP, destination,))
    runcmd('chmod +x %s' % (destination,))
    git.sudo('%s syncdb --migrate --noinput' % (destination,))
    git.sudo('%s collectstatic --noinput' % (destination,))
