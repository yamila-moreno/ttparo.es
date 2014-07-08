# -*- coding: utf-8 -*-

import os
from fabric.api import local, settings, abort, run, cd, env, put, get, prefix
from fabric.decorators import task, hosts, with_settings

HOME = '/home/yami'
REPO =  os.path.join(HOME, 'ttdp')
PROJECT = os.path.join(REPO, 'src')

def venv(command):
    basic_env_data = 'workon ttdp'
    return run('source {}/.bashrc && '
               'source /etc/bash_completion.d/virtualenvwrapper && '
               'source /etc/profile && '.format(HOME)
                + basic_env_data + ' && ' + command)


@task
@hosts('yami@robonia')
@with_settings(shell = '/bin/bash -c')
def deploy(**kwargs):
    with cd(REPO):
       run('git reset --hard')
       run('git checkout master')
       run('git pull')

    with cd(PROJECT):
        run('make')
        venv('pip install -r ../tools/requirements.txt')
        venv('python manage.py collectstatic --noinput')
