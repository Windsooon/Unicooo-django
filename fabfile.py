#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, re
from datetime import datetime

# import fabric api
from fabric.api import *

env.user = "root"

env.sudo_user = "root"

env.hosts = ["119.29.68.183"]

db_user = "db-user"

db_password = "db-password"


_TAR_FILE = "dist-unicooo.tar.gz"

def build():
    includes = ["activities", "api", "bin", "comment", "common", "log", "post", "public", "run", "templates", "unicooo", "*.py"]
    excludes = ['*.pyc', '*.pyo']
    with lcd(os.path.join(os.path.abspath('.'), 'www')):
        cmd = ['tar', '--dereference', '-czvf', '../dist/%s' % _TAR_FILE]
        cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
        cmd.extend(includes)
        local(' '.join(cmd))

_REMOTE_TMP_TAR = '/tmp/%s' % _TAR_FILE
_REMOTE_BASE_DIR = '/srv/unicooo'

def deploy():
    newdir = 'www-%s' % datetime.now().strftime('%y-%m-%d_%H.%M.%S')
    # 删除已有的tar文件:
    run('rm -rf %s' % _REMOTE_TMP_TAR)
    # 上传新的tar文件:
    put('dist/%s' % _TAR_FILE, _REMOTE_TMP_TAR)
    # 创建新目录:
    with cd(_REMOTE_BASE_DIR):
        sudo('mkdir %s' % newdir)
    # 解压到新目录:
    with cd('%s/%s' % (_REMOTE_BASE_DIR, newdir)):
        sudo('tar -xzvf %s' % _REMOTE_TMP_TAR)
    # 重置软链接:
    with cd(_REMOTE_BASE_DIR):
        sudo('rm -rf www')
        sudo('ln -s %s www' % newdir)
        sudo('chown windson:unicooo www')
        sudo('chown -R windson:unicooo %s' % newdir)
    # 重启Python服务和nginx服务器:
    with settings(warn_only=True):
        sudo('supervisorctl stop unicooo')
        sudo('supervisorctl start unicooo')

