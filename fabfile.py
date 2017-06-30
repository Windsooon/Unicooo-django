from fabric.contrib.files import exists, sed
from fabric.api import env, local, run
from fabric.operations import put

REPO_URL = 'git@github.com:Windsooon/Unicooo-django.git'


def deploy():
    if env.host == 'ec2-52-53-245-23.us-west-1.compute.amazonaws.com':
        env.host = 'stage.unicooo.com'
        host_pre = 'stage.unicooo'
    else:
        env.host = 'unicooo.com'
        host_pre = 'unicooo'

    site_folder = '/home/{0}/sites/{1}'.format(env.user, env.host)
    source_folder = site_folder + '/source'
    nginx_conf = (
        source_folder +
        '/nginx_pro/sites-enabled/unicooo_project.conf')
    _create_directory(site_folder)
    _get_latest_source(source_folder)
    _update_nginx(nginx_conf, host_pre, site_folder)
    _add_local_file(site_folder, source_folder)
    _update_compose(source_folder)
    _run_docker()


def _create_directory(site_folder):
    run('mkdir -p {0}'.format(site_folder))
    run('mkdir -p {0}/challenges/'.format(site_folder))
    run('mkdir -p {0}/ssl/'.format(site_folder))


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd {0} && git fetch'.format(source_folder))
    else:
        run('git clone {0} {1}'.format(REPO_URL, source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd {0} && git reset --hard {1}'.format(
        source_folder, current_commit))


def _update_nginx(nginx_conf, host_pre, site_folder):
    sed(
        nginx_conf, 'unicooo',
        host_pre, backup='')
    sed(
        nginx_conf, 'deploy_site',
        site_folder, backup='')


def _add_local_file(site_folder, source_folder):
    put('challenges', site_folder)
    put('ssl', site_folder)
    put('./www/common/qiniuSettings.py', source_folder + '/www/common/')


def _update_compose(source_folder):
    if env.host == 'stage.unicooo.com':
        sed(
            source_folder + '/docker-compose-pro.yml',
            'unicooo.settings.production',
            'unicooo.settings.stage',
            backup='')


def _run_docker():
    run('docker-compose -f docker-compose-pro.yml up -d --build')
