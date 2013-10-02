# -*- coding: utf-8 -*-

import os

from fabric.api import sudo


TPL_DIR = os.path.join(os.path.dirname(__file__), 'tpl')


def runcmd(arg):
    sudo("%s" % arg, pty=True)
