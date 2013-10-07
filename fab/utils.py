# -*- coding: utf-8 -*-

import os

from fabric.api import sudo


TPL_DIR = os.path.join(os.path.dirname(__file__), 'tpl')

FABRIC_ENV_PASSWORD = "vagrant"

FABRIC_ENV_ROLEDEFS = {
    'vagrant': ['vagrant@127.0.0.1:2222', ],
    }


def runcmd(arg):
    sudo("%s" % arg, pty=True)


def setup_fabric(env):
    env.password = FABRIC_ENV_PASSWORD
    env.roledefs.upadate(FABRIC_ENV_ROLEDEFS)
